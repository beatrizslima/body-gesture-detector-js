var robot = require("robotjs");
var util = require("./util");
//var poseDetection = require("./tensor")

var fs = require('fs')



async function init() {

  /*robot.typeString("B");
  await util.sleep(5000);
  robot.keyTap("e");
  robot.keyTap("enter");*/
  //await testBodyGesture()
  await testBodyGesture2()
  //await testMine()
}

async function testKeyMouseInput() {
  await util.sleep(5000);
  var goesUp = false;
  for (i = 0; i < 15; i++) {
    robot.keyToggle("w", "down")
    await util.sleep(500)
    robot.keyToggle("w", "up")

    let mPos = robot.getMousePos();
    console.log(mPos)
    robot.moveMouseSmooth((mPos.x + 100), (mPos.y + (goesUp ? 100 : -100)), 2)
    await util.sleep(0)
    goesUp = !goesUp
    robot.mouseClick();
  }
}

/*async function testBodyGesture() {

  c = fs.readFileSync(__dirname + 'assets/sampleImg1.jpg');
  p = new JPG(c);

  const model = poseDetection.SupportedModels.MoveNet;
  const detector = await poseDetection.createDetector(model);
  const poses = await detector.estimatePoses(image);
  //var detector = tensor.createDetector()
  //var poses = tensor.detectFromImage(detector, p)
}*/

function onResults(results) {
  console.log(results.poseWorldLandmarks)
}
async function testBodyGesture2() {

  defaultOptions = {
    selfieMode: false,
    modelComplexity: 0,
    smoothLandmarks: true,
    enableSegmentation: false,
    smoothSegmentation: true,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5,
    effect: 'background',
  }

  const options = {
    locateFile: (file) => {
      return `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.4/pose.js`;
    }
  };
  const pose = new mpPose.Pose(options);
  pose.onResults(onResults);
}

init()