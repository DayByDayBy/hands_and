import * as handPoseDetection from '@tensorflow-models/hand-pose-detection';

const model = handPoseDetection.SupportedModels.MediaPipeHands;
const detectorConfig = {
  runtime: 'mediapipe', // or 'tfjs'
  modelType: 'full'
};
detector = await handPoseDetection.createDetector(model, detectorConfig);

const video = document.getElementById('video');
const hands = await detector.estimateHands(video);


// via https://blog.tensorflow.org/2021/11/3D-handpose.html


//    shape of output:

// [
//     {
//       score: 0.8,
//       Handedness: 'Right',
//       keypoints: [
//         {x: 105, y: 107, name: "wrist"},
//         {x: 108, y: 160, name: "pinky_finger_tip"},
//         ...
//       ]
//       keypoints3D: [
//         {x: 0.00388, y: -0.0205, z: 0.0217, name: "wrist"},
//         {x: -0.025138, y: -0.0255, z: -0.0051, name: "pinky_finger_tip"},
//         ...
//       ]
//     }
//   ]