"""
Object Tracking Project - OpenCV
---------------------------------
This script tracks a single object across video frames.
It works with a live webcam or with a video file.

How it works (high level):
1. Read the first frame from the source (camera or video file).
2. Let the user draw a box around the object to track.
3. Create an OpenCV tracker (CSRT) and initialize it on that box.
4. For every next frame, ask the tracker "where did the object move?"
5. Draw the new box on the frame and show it.

Run examples:
    python object_tracker.py                     -> uses webcam (device 0)
    python object_tracker.py --source video.mp4   -> uses a video file
    python object_tracker.py --tracker KCF        -> use a faster/lighter tracker
"""

import cv2
import argparse
import time


def create_tracker(tracker_type: str):
    """Create an OpenCV tracker object based on the chosen algorithm.

    Different OpenCV versions expose the tracker classes in different
    places (cv2.TrackerCSRT_create, cv2.legacy.TrackerCSRT_create, etc).
    We try the known locations in order and use whichever works.
    """
    tracker_type = tracker_type.upper()
    candidates = []

    if tracker_type == "CSRT":
        candidates = ["TrackerCSRT_create", "legacy.TrackerCSRT_create"]
    elif tracker_type == "KCF":
        candidates = ["TrackerKCF_create", "legacy.TrackerKCF_create"]
    elif tracker_type == "MIL":
        candidates = ["TrackerMIL_create", "legacy.TrackerMIL_create"]
    else:
        raise ValueError(f"Unknown tracker type: {tracker_type}")

    for path in candidates:
        obj = cv2
        try:
            for part in path.split("."):
                obj = getattr(obj, part)
            return obj()
        except AttributeError:
            continue

    raise AttributeError(
        f"Could not find a '{tracker_type}' tracker in this OpenCV install. "
        f"Tried: {candidates}. Try: pip install opencv-contrib-python"
    )


def main():
    parser = argparse.ArgumentParser(description="OpenCV Object Tracking")
    parser.add_argument("--source", default="0",
                         help="Camera index (default 0) or path to a video file")
    parser.add_argument("--tracker", default="CSRT",
                         help="Tracker algorithm: CSRT, KCF, or MIL")
    parser.add_argument("--bbox", default=None,
                         help="Optional manual box 'x,y,w,h' to skip the "
                              "interactive selection (useful for testing)")
    parser.add_argument("--save", default=None,
                         help="Optional path to save the output video, e.g. output.mp4")
    parser.add_argument("--no-display", action="store_true",
                         help="Run without opening a live window (for headless testing)")
    parser.add_argument("--max-frames", type=int, default=None,
                         help="Stop after N frames (useful for testing)")
    args = parser.parse_args()

    # --- Step 1: open the video source (camera or file) ---
    source = int(args.source) if args.source.isdigit() else args.source
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"Error: could not open source {source}")
        return

    # Warm up the camera: the first few frames from a webcam are often
    # empty or black while the camera sensor is still initializing.
    # We read and discard a handful of frames before trusting the feed.
    ok, frame = False, None
    for attempt in range(30):
        ok, frame = cap.read()
        if ok and frame is not None and frame.mean() > 1:
            break
        time.sleep(0.1)

    if not ok or frame is None:
        print("Error: could not read a valid first frame from the camera.")
        print("Check that no other app (Zoom, Teams, browser tab, etc.) is using it,")
        print("and that Windows camera privacy settings allow desktop apps.")
        return

    # --- Step 2: get the bounding box of the object to track ---
    if args.bbox:
        x, y, w, h = map(int, args.bbox.split(","))
        bbox = (x, y, w, h)
    else:
        print("Draw a box around the object, then press ENTER or SPACE.")
        cv2.namedWindow("Select Object", cv2.WINDOW_NORMAL)
        cv2.imshow("Select Object", frame)
        cv2.waitKey(1)  # force the window to actually paint the frame
        bbox = cv2.selectROI("Select Object", frame, False)
        cv2.destroyWindow("Select Object")

    # --- Step 3: create and initialize the tracker ---
    tracker = create_tracker(args.tracker)
    tracker.init(frame, bbox)

    # Optional: set up video writer to save the result
    writer = None
    if args.save:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        h_frame, w_frame = frame.shape[:2]
        writer = cv2.VideoWriter(args.save, fourcc, 20.0, (w_frame, h_frame))

    frame_count = 0
    prev_time = time.time()

    while True:
        ok, frame = cap.read()
        if not ok:
            break  # end of video / camera disconnected

        # --- Step 4: update the tracker with the new frame ---
        ok, bbox = tracker.update(frame)

        # --- Step 5: draw the result ---
        if ok:
            x, y, w, h = [int(v) for v in bbox]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Tracking", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Lost", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # Show FPS so we can see tracking speed
        now = time.time()
        fps = 1.0 / (now - prev_time) if now != prev_time else 0.0
        prev_time = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        if writer is not None:
            writer.write(frame)

        if not args.no_display:
            cv2.imshow("Object Tracking", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        frame_count += 1
        if args.max_frames and frame_count >= args.max_frames:
            break

    cap.release()
    if writer is not None:
        writer.release()
    cv2.destroyAllWindows()
    print(f"Done. Processed {frame_count} frames.")


if __name__ == "__main__":
    main()
