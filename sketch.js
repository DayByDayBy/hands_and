let handPose;

let video;


function preload(){

    handPose = ml5.handPose();
}

function setup() {
    createCanvas(640, 480);
}