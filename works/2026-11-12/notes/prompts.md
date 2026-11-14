# 《车间双轨》素材生成记录

生成通道：MiniMax `image-01`（`/v1/image_generation`，`aspect_ratio=16:9`）
后处理：居中裁切至 1600×900 → JPEG（progressive, 4:2:0, optimize）→ 画质取「字节 ≤260000 的最高档」
约束：单张 ≤260KB（按 260,000 字节严口径卡）、画质 ≥80、长边 ≥1600px、图内无任何文字

## 图 A · 车间双轨全景（首屏背景氛围）

- 文件：`scene-a-workshop.jpg`（255323 bytes，1600×900，JPEG quality≈92）
- 底稿候选：MiniMax `image-01` 16:9 共 2 张中选第 2 张（人工核查无文字）

**prompt 原文（单行）**

```text
Photorealistic industrial factory hall interior, wide establishing shot down a long production aisle, cold blue-grey concrete floor, matte steel columns and overhead truss, two parallel glowing light tracks running from the foreground into a deep vanishing point, the left track emits a warm orange light band on the floor, the right track emits a cyan-blue light band, roller conveyor belts and crates along both tracks, several robotic arms standing as dark silhouettes along the lines, workstations with fixtures and cable trays, volumetric haze and soft god rays from overhead industrial lamps, cinematic wide angle 24mm, shallow depth of field, muted cold color grade with the two light bands as the only saturated elements, photographic realism, ultra detailed, 16:9, no text, no letters, no words, no numbers, no captions, no signage, no signage labels, no logo, no watermark, no UI, no watermark, no human face close-up, no cartoon, no illustration, no 3d render
```

## 图 B · 一句指令改写任务的瞬间

- 文件：`scene-b-rewrite.jpg`（256101 bytes，1600×900，JPEG quality≈95）
- 底稿候选：MiniMax `image-01` 16:9 共 4 张中选第 2 张（人工核查无文字）

**prompt 原文（单行）**

```text
Photorealistic industrial factory workcell, cold blue-grey palette, concrete floor and steel frame, a single robotic arm on a metal workbench in the middle of the frame, one narrow beam of amber warning light raking down onto the arm from above, the arm caught mid-move as its task is redirected, gripper twisting toward a different part, subtle motion blur on the moving joint, cold cyan rim light along the opposite edge of the machine, scattered metal parts on the bench, faint haze, dramatic single-source lighting, cinematic, photographic realism, ultra detailed, 16:9, no text, no letters, no words, no numbers, no captions, no signage, no signage labels, no logo, no watermark, no UI, no watermark, no human face close-up, no cartoon, no illustration, no 3d render
```

