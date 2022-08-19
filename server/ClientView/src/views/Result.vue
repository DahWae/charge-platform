<script setup>

import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import JSON5 from 'json5'
import {
    Row,
    Col,
    Circle,
} from 'vant'

const plate = window.location.search.substring(7)
const source = new EventSource(serverUrl + '/search/' + plate)

var currentRate = ref(0);
var text = ref(currentRate.value.toFixed(1) + '%')

onMounted(() => {
    source.addEventListener("new_message", newMessage);
})

onBeforeUnmount(() => {
    source.removeEventListener("new_message", newMessage)
})

function newMessage(e) {
    var data = JSON5.parse(e.data)

    if (data.percentage == -1)
        currentRate.value = NaN

    else
        currentRate.value = data.percentage;
        
    text.value = currentRate.value.toFixed(1) + '%'
    console.log(currentRate.value)
    console.log(text.value)
}

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
        <Circle v-model:current-rate="currentRate" :rate=currentRate :speed="100" :text=text :size="180"
            :stroke-width="80" />
        </Col>
    </Row>
</template>

<style>
:root {
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