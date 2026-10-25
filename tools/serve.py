"""
serve.py — showcase 本地预览服务器（带私有目录访问拦截）

用法：
  python3 tools/serve.py            # 默认 8940 端口
  python3 tools/serve.py 9000       # 指定端口

为什么需要：
  showcase 目录同时存放「对外作品」和「内部文件」（备份、归档、构建脚本）。
  直接 `python3 -m http.server` 会把 _private/、_archive/、tools/ 一并暴露。
  本脚本对这三类路径返回 403，仅允许作品与静态资源访问。
"""

import http.server, os, socketserver, sys

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8940
# 默认只监听本机。展厅是内部使用（AGENTS.md：内部使用，不做公开 SEO），
# 绑 0.0.0.0 等于把整个目录挂到局域网上 —— 实测过的教训。
# 需要局域网访问时显式传 --lan。
HOST = '0.0.0.0' if '--lan' in sys.argv else '127.0.0.1'
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCKED_PREFIXES = ('_private', '_archive', 'tools', 'templates', '.git',
                    '__pycache__', '.impeccable', 'notes')


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _blocked(self):
        rel = self.path.split('?')[0].lstrip('/')
        # 检查**所有目录段**，不只首段：过程材料在 YYYY-MM-DD/notes/ 下，
        # 只拦首段的话 notes/ 实际是暴露的（实测发现的漏洞）。
        # 末段是文件名，不参与判断 —— 否则 slug 含 notes 的作品会被误拦。
        segs = rel.split('/')
        return any(s in BLOCKED_PREFIXES for s in segs[:-1])

    def send_error(self, code, message=None, explain=None):
        if code == 404 and self._blocked():
            code, message = 403, 'Forbidden'
            explain = '私有目录不对外提供访问'
        super().send_error(code, message, explain)

    def do_GET(self):
        if self._blocked():
            self.send_error(404)
            return
        super().do_GET()

    def do_HEAD(self):
        if self._blocked():
            self.send_error(404)
            return
        super().do_HEAD()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


class Server(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    with Server((HOST, PORT), Handler) as httpd:
        print(f'showcase 预览：http://{HOST}:{PORT}/index.html')
        if HOST != '127.0.0.1':
            print('  ⚠ 已监听 0.0.0.0 —— 局域网内其他设备可访问')
        print(f'已拦截私有路径：{", ".join(BLOCKED_PREFIXES)}')
        httpd.serve_forever()
