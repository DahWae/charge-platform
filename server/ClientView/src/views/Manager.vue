<script setup>
import {
    ref
} from 'vue'

import JSON5 from 'json5'

import {
    Button,
    Row,
    Col,
    Icon,
    Image,
    Circle,
    Divider,
} from 'vant'

const appBody = document.getElementById('app');
const robotEvtSource = new EventSource(serverUrl + '/robot');
const vehicleEvtSource = new EventSource(serverUrl + '/vehicle');

var robotCount = 0;

robotEvtSource.addEventListener("new_message", (e) => {

    // console.log(e.data);
    var data = JSON5.parse(e.data)
    var newEl = document.createElement('div')
    document.createAttribute()
    var newText = document.createTextNode('test here');

    newEl.appendChild(newText)
    newEl.id = 'robot-' + i
    // console.log(data)
    // console.log(Object.keys(data).length)

    // document.getElementById('displayTest').innerText = data.data1;
    // var insertPoint = document.getElementById('myDivider');
    // appBody.insertBefore(testDiv, insertPoint);
});

vehicleEvtSource.addEventListener("new_message", (e) => {
    // console.log(e.data);
    var data = JSON5.parse(e.data)
    // console.log(data)
    // console.log(Object.keys(data).length)

})

function addRobot() {
    const elSpan = [2, 2, 3, 5, 5, 2, 2]
    const elName = ["x", "y", "target", "robotStatus", "amrStatus", "amrBattery", "amrTemperature"]
    const insertPoint = document.getElementById('myDivider');

    var newRobot = document.createElement("div");
    newRobot.setAttribute("class", "van-row van-row--justify-center");

    newRobot.id = 'robot-' + robotCount;
    robotCount += 1;

    for (var i = 0; i < elSpan.length; i++) {
        var newCol = document.createElement("div");
        newCol.setAttribute("class", "van-col van-col--" + elSpan[i]);

        newCol.id = newRobot.id + '-' + elName[i];
        var testContext = document.createTextNode('tst');
        newCol.appendChild(testContext);
        // newCol.innerText = elSpan[i];
        newRobot.appendChild(newCol)
    }
    
    console.log(insertPoint)
    appBody.insertBefore(newRobot, insertPoint)


}

function addVehicle() {

}


window.onload = function () {
    addRobot()
    // var testDiv = document.createElement('div')
    // var testContext = document.createTextNode('test insert here');
    // testDiv.appendChild(testContext);

    // var insertPoint = document.getElementById('myDivider');
    // appBody.insertBefore(testDiv, insertPoint);
}


</script>


<template>
    <Row justify="center">
        <Col span="24" style="position:relative;">
        <img alt="map" style="width:70%;" src="@/assets/map.png" />
        <Icon style="z-index: 20;position: absolute;top: 25%;left: 20%;" name="circle" color="red" />
        </Col>
    </Row>

    <Row justify="center">
        <div class="manager">
            <h2>Manager</h2>
        </div>
    </Row>

    <Row justfy="center">
        <Col span="24">
        <div class="robots">
            for Robots
        </div>
        <div id="displayTest">
            display test
        </div>
        </Col>

    </Row>
    <Row justify="center">
        <Col span="2">
        <div id="robotX">
            x
        </div>
        </Col>
        <Col span="2">
        <div id="robotY">
            y
        </div>
        </Col>
        <Col span="3">
        <div id="robotTarget">
            tgt
        </div>
        </Col>
        <Col span="5">
        <div id="robotStatus">
            charge
        </div>
        </Col>
        <Col span="5">
        <div id="amrStatus">
            no task
        </div>
        </Col>
        <Col span="2">
        <div id="amrBattery">
            80
        </div>
        </Col>
        <Col span="2">
        <div id="amrTemp">
            20
        </div>
        </Col>
    </Row>

    <Divider id="myDivider" :style="{ height: '5px', borderColor: '#1989fa', padding: '0 16px' }" />

    <Row justify="center">
        <Col span="24">
        <div class="tasks">
            for Tasks
        </div>
        </Col>
    </Row>

</template>

<style>
.manager {
    margin: 8px;
}
</style>