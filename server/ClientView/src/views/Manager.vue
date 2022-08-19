<script setup>
import { onBeforeUnmount, onMounted } from 'vue';
import axios from 'axios'
import JSON5 from 'json5'
import {
    Button,
    Row,
    Col,
    Icon,
    Image,
    Circle,
    Divider,
    Toast,
} from 'vant'

const appBody = document.getElementById('app');
const robotEvtSource = new EventSource(serverUrl + '/robot');
const vehicleEvtSource = new EventSource(serverUrl + '/vehicle');

var robotCount = 0;
var vehicleCount = 0;

onMounted(() => {
    robotEvtSource.addEventListener("new_message", newRobotMessage);
    vehicleEvtSource.addEventListener("new_message", newvehicleMessage);
})

onBeforeUnmount(() => {
    robotEvtSource.removeEventListener("new_message", newRobotMessage);
    vehicleEvtSource.removeEventListener("new_message", newvehicleMessage);
})

function newRobotMessage(e) {
    const elName = ["x", "y", "target", "robotStatus", "amrBattery", "amrTemperature"]

    var data = JSON5.parse(e.data)

    // var newEl = document.createElement('div')
    // document.createAttribute()
    // var newText = document.createTextNode('test here');

    // newEl.appendChild(newText)
    // newEl.id = 'robot-' + i

    for (var i = 0; i < data.length; i++) {
        var robotID = "robot-" + i;
        if (document.getElementById(robotID) == null)
            addRobot()

        var elementID = robotID + "-" + elName[0];
        document.getElementById(elementID).innerText = data[i].position.x.toFixed(2)

        elementID = robotID + "-" + elName[1];
        document.getElementById(elementID).innerText = data[i].position.y.toFixed(2)

        elementID = robotID + "-" + elName[2];
        document.getElementById(elementID).innerText = data[i].robot.robotTarget

        elementID = robotID + "-" + elName[3];
        document.getElementById(elementID).innerText = data[i].robot.robotStatus

        elementID = robotID + "-" + elName[4];
        document.getElementById(elementID).innerText = data[i].robot.amrBattery.toFixed(0)

        elementID = robotID + "-" + elName[5];
        document.getElementById(elementID).innerText = (+(data[i].robot.amrTemp)).toFixed(0)
    }

    deleteRobot(i);

    // console.log(data)
    // console.log(Object.keys(data).length)

    // document.getElementById('displayTest').innerText = data.data1;
    // var insertPoint = document.getElementById('myDivider');
    // appBody.insertBefore(testDiv, insertPoint);

}

function newvehicleMessage(e) {

    const elName = ["ts", "plate", "parkID", "power", "pickTime", "percentage", "status", "delete"]

    var data = JSON5.parse(e.data)

    console.log(data)
    if (data == null)
        return

    for (var i = 0; i < data.length; i++) {
        var vehicleID = "vehicle-" + i;
        if (document.getElementById(vehicleID) == null)
            addVehicle()

        var elementID = vehicleID + "-" + elName[0];
        document.getElementById(elementID).innerText = data[i].ts

        elementID = vehicleID + "-" + elName[1];
        document.getElementById(elementID).innerText = data[i].plate

        elementID = vehicleID + "-" + elName[2];
        document.getElementById(elementID).innerText = data[i].parkID

        elementID = vehicleID + "-" + elName[3];
        document.getElementById(elementID).innerText = data[i].power

        elementID = vehicleID + "-" + elName[4];
        document.getElementById(elementID).innerText = data[i].pickTime

        elementID = vehicleID + "-" + elName[5];
        document.getElementById(elementID).innerText = data[i].percentage.toFixed(0)

        elementID = vehicleID + "-" + elName[6];
        document.getElementById(elementID).innerText = data[i].status
    }

    deleteVehicle(i);
}

function setAttributes(el, attrs) {
    for (var key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}

function addRobot() {
    // ts, plate, parkID, power, pickTime, percentage, status
    const elSpan = [3, 3, 5, 5, 2, 2]
    const elName = ["x", "y", "target", "robotStatus", "amrBattery", "amrTemperature"]
    const insertPoint = document.getElementById('divider-1');

    var newRobot = document.createElement("div");
    setAttributes(newRobot, { "class": "listElement van-row van-row--justify-center" });

    newRobot.id = 'robot-' + robotCount;
    robotCount += 1;

    for (var i = 0; i < elSpan.length; i++) {
        var newCol = document.createElement("div");
        setAttributes(newCol, { "class": "van-col van-col--" + elSpan[i] });
        newCol.id = newRobot.id + "-" + elName[i];
        var testContext = document.createTextNode('tst');
        newCol.appendChild(testContext);
        newRobot.appendChild(newCol)
    }

    appBody.insertBefore(newRobot, insertPoint)


}

function addVehicle() {
    const elSpan = [3, 4, 2, 3, 3, 2, 2, 2]
    const elName = ["ts", "plate", "parkID", "power", "pickTime", "percentage", "status", "delete"]
    const insertPoint = document.getElementById('divider-2');

    var newVehicle = document.createElement("div");
    setAttributes(newVehicle, { "class": "listElement van-row van-row--justify-center" });

    newVehicle.id = 'vehicle-' + vehicleCount;
    vehicleCount += 1;

    var deleteButton = document.createElement("button");
    setAttributes(deleteButton, { "type": "button", "class": "van-button van-button--danger van-button--mini van-button--round" });
    var buttonContent = document.createElement("div");
    setAttributes(buttonContent, { "class": "van-button__content" });
    var iconContent = document.createElement("i");
    setAttributes(iconContent, { "class": "van-badge__wrapper van-icon van-icon-minus van-button__icon" });
    buttonContent.appendChild(iconContent);
    deleteButton.appendChild(buttonContent);

    deleteButton.onclick = function () { deleteTask(document.getElementById(newVehicle.id + "-" + elName[0]).innerText) }

    for (var i = 0; i < elSpan.length; i++) {
        var newCol = document.createElement("div");
        setAttributes(newCol, { "class": "van-col van-col--" + elSpan[i] });
        newCol.id = newVehicle.id + "-" + elName[i];
        var newContext = document.createTextNode('tst');
        if (i == elSpan.length - 1)
            newCol.appendChild(deleteButton);
        else
            newCol.appendChild(newContext);
        newVehicle.appendChild(newCol);
    }


    appBody.insertBefore(newVehicle, insertPoint)

}

function deleteTask(elementID) {
    console.log(elementID);
    axios.post(serverUrl + '/delete', {ts: elementID})
        .then(function (response) {
            console.log(response);
            Toast(response.statusText);
        })
        .catch(function (error) {
            console.log(error);
            Toast('ERROR');
        })
}

function deleteRobot(num) {
    for (var i = num; document.getElementById("robot-" + i) != null; i++) {
        document.getElementById("robot-" + i).remove();
    }
}

function deleteVehicle(num) {
    for (var i = num; document.getElementById("vehicle-" + i) != null; i++) {
        document.getElementById("vehicle-" + i).remove();
    }
}

window.onload = function () {
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

    <Row justify="center" class="listElement">
        <Col span="3">
        <div id="robotX">
            x
        </div>
        </Col>
        <Col span="3">
        <div id="robotY">
            y
        </div>
        </Col>
        <Col span="5">
        <div id="robotTarget">
            Target
        </div>
        </Col>
        <Col span="5">
        <div id="robotStatus">
            Status
        </div>
        </Col>
        <Col span="2">
        <div id="amrBattery">
            %
        </div>
        </Col>
        <Col span="2">
        <div id="amrTemp">
            C
        </div>
        </Col>
    </Row>

    <Divider id="divider-1" :style="{ height: '5px', borderColor: '#1989fa', padding: '0 16px' }" />


    <Row justify="center" class="listElement">
        <Col span="3">
        <div id="ts">
            ts
        </div>
        </Col>
        <Col span="4">
        <div id="plate">
            plate
        </div>
        </Col>
        <Col span="2">
        <div id="parkID">
            ID
        </div>
        </Col>
        <Col span="3">
        <div id="power">
            pow
        </div>
        </Col>
        <Col span="3">
        <div id="pickTime">
            pick
        </div>
        </Col>
        <Col span="2">
        <div id="percentage">
            %
        </div>
        </Col>
        <Col span="2">
        <div id="status">
            stat
        </div>
        </Col>
        <Col span="2">
        <div id="delete">
            del
        </div>
        </Col>
    </Row>

    <Divider id="divider-2" :style="{ height: '5px', borderColor: '#1989fa', padding: '0 16px' }" />

</template>

<style>
.manager {
    margin: 3px;
}

.listElement {
    font-size: small;
    display: flex;
    align-items: center;
}
</style>