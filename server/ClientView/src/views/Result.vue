<script setup>

import { ref, computed } from 'vue';
import {
    Row,
    Col,
    Circle,
} from 'vant'

var currentRate = ref(30);
var text = computed(() => currentRate.value.toFixed(0) + '%')

</script>


<template>
    <Row justify="center">
        <Col span="24">
            <h1>{{ $route.query.plate }}</h1>
        </Col>
    </Row>

    <div class="gap-30" />

    <Row justify="center">
        <Col span="24">
        <Circle v-model:current-rate="currentRate" :rate=currentRate :speed="100" :text=text :size="180" :stroke-width="80"  />
        </Col>
    </Row>
</template>

<style>
:root{
    --van-circle-text-font-size: 35px;
}

.gap {
    margin: 16px;
}

.gap-30 {
    width: 100%;
    height: 30px;
}

</style>