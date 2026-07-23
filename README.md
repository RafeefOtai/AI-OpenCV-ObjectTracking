# AI Task 2 - Object Tracking (OpenCV)

## ▶️ [Watch the Tracking Video](https://drive.google.com/file/d/1jgoyIhErwdcBpYtw5Vjv-ijOAY1X1PST/view?usp=drivesdk)
> Notes : Tracking works best while the object stays visible in frame. If it's lost, it needs to be re-selected to continue.

---

## What Object Tracking means 

Object detection finds an object in a single frame. Tracking is different: the object is selected once, and the algorithm follows that same object frame after frame without re-detecting it every time. This makes tracking more efficient than running object detection on every frame.

---

## Requirements
```bash
pip install opencv-contrib-python
```
The contrib build is needed because the tracker classes (CSRT, KCF, MIL)
aren't guaranteed to be in the base `opencv-python` package on newer
OpenCV versions.

---

## Running it
```bash
python object_tracker.py
```
`--source` swaps in a video file instead of the webcam, `--save` writes
the result to a file, `--tracker` switches the algorithm (CSRT is
default). The first frame opens a window to draw a box around the object;
tracking starts once it's confirmed.

---

## Supported Trackers

| Tracker | Speed | Accuracy | Best for |
|----------|------:|---------:|----------|
| CSRT | Slower | Highest | General object tracking |
| KCF | Faster | Medium | Real-time performance |
| MIL | Medium | Lower | Simple tracking tasks |
