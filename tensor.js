
var poseDetection = require('@tensorflow-models/pose-detection');
var tfjscore = require('@tensorflow/tfjs-core');
// Register WebGL backend.
require('@tensorflow/tfjs-backend-webgl');
require('@mediapipe/pose');

async function createDetector(){
  const model = poseDetection.SupportedModels.BlazePose;
  const detectorConfig = {
    runtime: 'mediapipe',
    solutionPath: 'base/node_modules/@mediapipe/pose'
  };
  return await poseDetection.createDetector(model, detectorConfig);
}

async function detectFromImage(detector, image){

  const estimationConfig = {enableSmoothing: true};
  return await detector.estimatePoses(image, estimationConfig);
}

module.exports = {createDetector, detectFromImage}