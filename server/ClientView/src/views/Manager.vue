<script setup>
import {
    ref
} from 'vue'

import {
    Button,
    Row,
    Col,
    Image,
    Circle,
} from 'vant'


</script>


<template>
    <Row justify="center">
        <img alt="map" width="300" height="300" src="@/assets/map.png" />
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