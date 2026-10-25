
(function(){
  "use strict";
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- progress bar ---------- */
  var prog = document.getElementById('progress');
  function onScroll(){
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? (window.pageYOffset / h) * 100 : 0;
    prog.style.width = p.toFixed(2) + '%';
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- reveal on scroll ---------- */
  var revs = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, {threshold:0.12, rootMargin:'0px 0px -8% 0px'});
    revs.forEach(function(el){ io.observe(el); });
  } else {
    revs.forEach(function(el){ el.classList.add('in'); });
  }

  /* ---------- counters ---------- */
  function fmt(el, v){
    var dec = parseInt(el.getAttribute('data-dec') || '0', 10);
    var s = (dec > 0) ? v.toFixed(dec) : Math.round(v).toLocaleString('en-US');
    var p = el.getAttribute('data-prefix') || '';
    var q = el.getAttribute('data-suffix') || '';
    return p + s + q;
  }
  function runCount(el){
    var target = parseFloat(el.getAttribute('data-count'));
    if (isNaN(target)) return;
    if (reduce){ el.textContent = fmt(el, target); return; }
    var dur = 1250, t0 = null;
    function step(ts){
      if (t0 === null) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur);
      var e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(el, target * e);
      if (p < 1) requestAnimationFrame(step);
      else el.textContent = fmt(el, target);
    }
    requestAnimationFrame(step);
  }
  var counters = Array.prototype.slice.call(document.querySelectorAll('[data-count]'));
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ runCount(e.target); co.unobserve(e.target); }
      });
    }, {threshold:0.4});
    counters.forEach(function(el){ co.observe(el); });
  } else {
    counters.forEach(runCount);
  }

  /* ---------- SCISSORS BLADE ---------- */
  var stage   = document.getElementById('stage');
  var grid    = document.getElementById('specimens');
  var rail    = document.getElementById('rail');
  var blade   = document.getElementById('blade');
  var range   = document.getElementById('blrange');
  var specs   = Array.prototype.slice.call(grid.querySelectorAll('.spec'));
  var railBtns= Array.prototype.slice.call(rail.querySelectorAll('.rail-labels button'));
  var roPct   = document.getElementById('ro-pct');
  var roCount = document.getElementById('ro-count');
  var roMood  = document.getElementById('ro-mood');
  var roNote  = document.getElementById('ro-note');
  var X = 46;

  specs.forEach(function(s){
    var d = document.createElement('div');
    d.className = 'dyn w';
    d.textContent = '被铺开';
    s.appendChild(d);
  });

  function isNarrow(){ return window.matchMedia('(max-width: 760px)').matches; }

  function computeCuts(){
    var cuts = [];
    if (isNarrow()) {
      // single column: the blade sweeps top-to-bottom through the stack
      for (var i = 0; i < specs.length; i++){
        var stepF = (X / 100) * specs.length - i;
        cuts.push(Math.max(0, Math.min(1, stepF)));
      }
    } else {
      var g = grid.getBoundingClientRect();
      var gw = g.width || 1;
      for (var j = 0; j < specs.length; j++){
        var r = specs[j].getBoundingClientRect();
        var left  = (r.left  - g.left) / gw * 100;
        var right = (r.right - g.left) / gw * 100;
        var w = Math.max(0.0001, right - left);
        cuts.push(Math.max(0, Math.min(1, (X - left) / w)));
      }
    }
    return cuts;
  }

  function paint(){
    var cuts = computeCuts();
    var touched = 0, full = 0, sum = 0;
    for (var i = 0; i < specs.length; i++){
      var f = cuts[i], s = specs[i];
      var cold = s.querySelector('.layer.cold');
      var cut  = s.querySelector('.cutline');
      var dyn  = s.querySelector('.dyn');
      cold.style.clipPath = 'inset(0 ' + ((1 - f) * 100).toFixed(2) + '% 0 0)';
      if (f > 0.001 && f < 0.999){
        cut.style.left = (f * 100).toFixed(2) + '%';
        cut.classList.add('on');
      } else {
        cut.classList.remove('on');
      }
      if (f <= 0.001){ dyn.className = 'dyn w'; dyn.textContent = '被铺开'; }
      else if (f >= 0.999){ dyn.className = 'dyn x'; dyn.textContent = '已被管制'; full++; }
      else { dyn.className = 'dyn mid'; dyn.textContent = '正在剪 ' + Math.round(f * 100) + '%'; }
      if (f > 0) touched++;
      sum += f;
    }
    var avg = sum / specs.length;
    blade.style.left = X + '%';
    blade.setAttribute('aria-valuenow', Math.round(X));
    blade.setAttribute('aria-valuetext', '剪刀开合度 ' + Math.round(X) + '%');
    range.value = Math.round(X);
    roPct.textContent = Math.round(X) + '%';
    roCount.innerHTML = touched + '<small> / ' + specs.length + '</small>';
    var mood, note;
    if (avg < 0.08){ mood = '全面铺开'; note = '技术基本不受限，注意力全在落地应用'; }
    else if (avg < 0.35){ mood = '铺开为主'; note = '管制线刚起，尚未覆盖到技术本身'; }
    else if (avg < 0.62){ mood = '两刃相抵'; note = '铺开与设限在同一批技术上正面相遇'; }
    else if (avg < 0.88){ mood = '设限为主'; note = '管制范围正在覆盖已铺开的技术'; }
    else { mood = '全面设限'; note = '前沿技术几乎全部进入许可与登记轨道'; }
    roMood.textContent = mood;
    roNote.textContent = note + '（' + full + ' 项已完全进入管制）';
    railBtns.forEach(function(b){
      var v = parseInt(b.getAttribute('data-pos'), 10);
      b.classList.toggle('on', Math.abs(v - X) < 6);
    });
  }

  function setX(v){
    X = Math.max(0, Math.min(100, v));
    paint();
  }

  function railPct(clientX){
    var r = rail.getBoundingClientRect();
    if (r.width <= 0) return X;
    return ((clientX - r.left) / r.width) * 100;
  }

  var dragging = false;
  function onDown(e){
    dragging = true;
    blade.setPointerCapture && blade.setPointerCapture(e.pointerId);
    setX(railPct(e.clientX));
    e.preventDefault();
  }
  blade.addEventListener('pointerdown', onDown);
  window.addEventListener('pointermove', function(e){ if (dragging) setX(railPct(e.clientX)); });
  window.addEventListener('pointerup', function(){ dragging = false; });
  window.addEventListener('pointercancel', function(){ dragging = false; });

  rail.addEventListener('click', function(e){
    if (e.target.closest('.rail-labels')) return;
    setX(railPct(e.clientX));
  });
  railBtns.forEach(function(b){
    b.addEventListener('click', function(){ setX(parseInt(b.getAttribute('data-pos'), 10)); });
  });
  range.addEventListener('input', function(){ setX(parseFloat(range.value)); });
  blade.addEventListener('keydown', function(e){
    var k = e.key;
    if (k === 'ArrowLeft'){ setX(X - 2); e.preventDefault(); }
    else if (k === 'ArrowRight'){ setX(X + 2); e.preventDefault(); }
    else if (k === 'Home'){ setX(0); e.preventDefault(); }
    else if (k === 'End'){ setX(100); e.preventDefault(); }
  });
  window.addEventListener('resize', function(){ paint(); });
  paint();

  /* ---------- 40-ITEM CATALOG ---------- */
  var rows = Array.prototype.slice.call(document.querySelectorAll('#list .row'));
  var domChips = Array.prototype.slice.call(document.querySelectorAll('#f-dom .chip'));
  var typeChips = Array.prototype.slice.call(document.querySelectorAll('#f-type .chip'));
  var fcN = document.getElementById('fc-n');
  var curDom = 'all', curType = 'all';

  function applyFilter(){
    var n = 0;
    rows.forEach(function(r){
      var ok = (curDom === 'all' || r.getAttribute('data-dom') === curDom) &&
               (curType === 'all' || r.getAttribute('data-type') === curType);
      r.style.display = ok ? '' : 'none';
      if (ok) n++;
    });
    fcN.textContent = n;
  }
  function bindChips(list, apply){
    list.forEach(function(c){
      c.addEventListener('click', function(){
        list.forEach(function(o){ o.classList.remove('on'); });
        c.classList.add('on');
        apply(c.getAttribute('data-v'));
      });
    });
  }
  bindChips(domChips, function(v){ curDom = v; applyFilter(); });
  bindChips(typeChips, function(v){ curType = v; applyFilter(); });
  applyFilter();

  rows.forEach(function(r){
    var head = r.querySelector('.head');
    var body = r.querySelector('.body');
    head.addEventListener('click', function(){
      var open = r.classList.toggle('open');
      body.style.maxHeight = open ? body.scrollHeight + 'px' : '0px';
    });
  });

  /* ---------- THRESHOLD JUDGE ---------- */
  var jParam = document.getElementById('j-param');
  var jFlop  = document.getElementById('j-flop');
  var jRank  = document.getElementById('j-rank');
  var jParamV= document.getElementById('j-param-v');
  var jFlopV = document.getElementById('j-flop-v');
  var jRankV = document.getElementById('j-rank-v');
  var vBox = document.getElementById('v-box');
  var vLv  = document.getElementById('v-lv');
  var vBig = document.getElementById('v-big');
  var vWhy = document.getElementById('v-why');
  var vRec = document.getElementById('v-rec');
  var dataSel = 'pub', sceneSel = 'normal', agentSel = 'no';

  function segBind(id, setter){
    var btns = Array.prototype.slice.call(document.querySelectorAll('#' + id + ' button'));
    btns.forEach(function(b){
      b.addEventListener('click', function(){
        btns.forEach(function(o){ o.classList.remove('on'); });
        b.classList.add('on');
        setter(b.getAttribute('data-v'));
        judge();
      });
    });
  }
  segBind('j-data',  function(v){ dataSel = v; });
  segBind('j-scene', function(v){ sceneSel = v; });
  segBind('j-agent', function(v){ agentSel = v; });

  var SUPS = ['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹'];
  function sup(n){ return String(n).replace(/[0-9]/g, function(d){ return SUPS[+d]; }); }
  function supDot(n){
    var s = String(n);
    var parts = s.split('.');
    return sup(parts[0]) + (parts[1] ? '·' + sup(parts[1]) : '');
  }

  function judge(){
    var paramT = parseInt(jParam.value, 10) / 10;           // 万亿参数
    var flopE  = 24 + Math.round(parseInt(jFlop.value, 10) / 2.5) / 10;
    var rank   = parseInt(jRank.value, 10);
    var agentHigh = (agentSel === 'yes');

    jParamV.textContent = paramT.toFixed(1) + ' 万亿';
    jFlopV.textContent  = '10' + supDot(flopE.toFixed(1)) + ' FLOPs';
    jRankV.textContent  = '第 ' + rank + ' 名';

    var bans = [], rests = [];
    if (dataSel === 'core'){
      bans.push({code:'266501J', t:'利用我国核心数据进行训练后提供服务的大模型'});
    }
    if (agentHigh && sceneSel === 'sensitive'){
      bans.push({code:'266502J', t:'高敏感场景（关基/国防军工/核心政务）中的高性能智能体'});
    }
    if (dataSel === 'imp'){
      rests.push({code:'266504X ①', t:'利用我国重要数据进行训练后提供服务的大模型'});
    }
    if (paramT >= 2){
      rests.push({code:'266504X ②', t:'参数量 ' + paramT.toFixed(1) + ' 万亿，已达 2 万亿红线'});
    }
    if (flopE >= 26){
      rests.push({code:'266504X ②', t:'训练算力 10' + supDot(flopE.toFixed(1)) + ' FLOPs，已达 10²⁶ 红线'});
    }
    if (rank <= 10){
      rests.push({code:'266504X ②', t:'公开评估全球第 ' + rank + ' 名，跻身前 10'});
    }

    vBox.className = 'verdict';
    var rec = '';
    if (bans.length){
      vBox.classList.add('ban');
      vLv.textContent = '禁止出口';
      vBig.textContent = '这类模型不能出口';
      vWhy.innerHTML = '触发 ' + bans.length + ' 条禁止类条款：' +
        bans.map(function(b){ return '<b>' + b.code + '</b> ' + b.t; }).join('；') + '。';
      rec = '<b>可走的路：</b><ul>' +
        '<li>停止用我国核心数据训练后对外提供服务，转为境内部署或以清洗后的重要数据训练</li>' +
        '<li>若属高敏感场景，把高性能智能体能力留在关基体系内部</li>' +
        '<li>对外以 API / APP / SaaS / 端侧轻量化形式提供服务，或通过开放权重绕开"技术转移"认定</li></ul>';
    } else if (rests.length){
      vBox.classList.add('restrict');
      vLv.textContent = '限制出口（需申请许可）';
      vBig.textContent = '核心受限，模型本身不违法';
      vWhy.innerHTML = '触发 ' + rests.length + ' 条限制类条款：' +
        rests.map(function(b){ return '<b>' + b.code + '</b> ' + b.t; }).join('；') + '。';
      rec = '<b>可走的路：</b><ul>' +
        '<li>模型权重、检查点、源码、架构与训练优化技术的对外转让，需申请技术出口许可证</li>' +
        '<li>已在海外自有云等风险可控情形下部署，可适用自动许可等便利措施</li>' +
        '<li>将核心技术开源、或赴境外流片、联合研发、参与国际标准制定，基本实现"即报即出"</li>' +
        '<li>正式目录落地前，先在商务部技术贸易管理信息应用完成出口前登记</li></ul>';
    } else {
      vBox.classList.add('free');
      vLv.textContent = '不纳入管理范围';
      vBig.textContent = '这个模型可以自由出海';
      vWhy.innerHTML = '没有触发任何一条禁止或限制条款。' +
        (dataSel === 'tiny' ? '微量重要数据（≤0.1%）经脱敏清洗、且不在输出中复现，已被明确排除在管理范围之外。' : '');
      rec = '<b>可走的路：</b><ul>' +
        '<li>直接出海，无需就核心技术申请许可</li>' +
        '<li>保持公开数据训练与公开测评排名的透明度，避开"全球前 10"与重要数据两条线</li>' +
        '<li>留意征求意见期内的指标调整，11 月 15 日前可提交意见</li></ul>';
    }
    vRec.innerHTML = rec;
  }
  [jParam, jFlop, jRank].forEach(function(el){ el.addEventListener('input', judge); });
  judge();
})();
