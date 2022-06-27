<script setup>

import {
    Row,
    Col,
} from 'vant'



</script>


<template>
    <Row justify="center">
        <div class="manager">
            <font> size="1">manager</font>
        </div>
    </Row>

    <Row justify="center">
        <Col span="24">
        <h1>{{ $route.params.plate }}</h1>
        <router-view/>
        </Col>
    </Row>
</template>

<style>
.gap {
    margin: 16px;
}
</style>