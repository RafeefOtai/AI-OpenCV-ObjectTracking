# AI Task 2 - Object Tracking (OpenCV)

## What Object Tracking means

Object detection finds an object in a single frame. Tracking is different:
the object is selected once, and the algorithm follows that same object
frame after frame, without re-detecting it every time. This makes tracking
more efficient than running object detection on every frame.

## Requirements

This project was developed using:

- Python 3.13.9
- OpenCV
- Webcam 

The required library can be installed using:

```bash
pip install opencv-contrib-python
```

## Project Execution

The project supports the following execution modes.

Using the default webcam:

```bash
python object_tracker.py
```

Using a video file as the input source:

```bash
python object_tracker.py --source my_video.mp4
```

Saving the tracking result to a new video file:

```bash
python object_tracker.py --source my_video.mp4 --save output.mp4
```

Using a different tracking algorithm:

```bash
python object_tracker.py --tracker KCF
```

When the first frame is displayed, the target object is selected by drawing
a bounding box around it. Tracking begins immediately after the selection
is confirmed.

## Supported Trackers

| Tracker | Speed | Accuracy | Best for |
|----------|------:|---------:|----------|
| CSRT | Slower | Highest | Default choice, good general accuracy |
| KCF | Faster | Medium | Real-time on weaker hardware |
| MIL | Medium | Lower | Simple test cases |

## Notes

- Tracking works best when the selected object remains visible and stays
  within the camera frame.
- If tracking is lost, the object must be selected again before tracking
  can continue.
