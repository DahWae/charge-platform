<script setup>
import {
    ref
} from 'vue'

import {
    Button,
    Row,
    Col,
    Icon,
    Image,
    Circle,
} from 'vant'


</script>


<template>
    <Row justify="center">
        <Col span="8" style="position:relative;">
                <img alt="map" style="width:100%;"  src="@/assets/map.png" />
                    <Icon style="z-index: 20;position: absolute;top: 25%;left: 20%;" name="circle" color="red"/>
        </Col>
        <Col span="8">
            This is for Robots information
        </Col>
    </Row>
    <Row justify="center">
        <div class="manager">
            <h1>Manager</h1>
        </div>
    </Row>



</template>

<style>
.manager {
    margin: 16px;
}
</style>