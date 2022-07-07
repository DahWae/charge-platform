<script setup>
import {
    Button,
    Row,
    Col,
    Image,
    Toast,
} from 'vant'

import axios from 'axios'

const onTest = () => {
    axios.get('http://127.0.0.1:8000/')
        .then(function (response) {
            console.log(response.data)
            Toast(response.data)
        })
};
</script>

<template>

    <div class="gap-30" />
    <Row justify="center">
        <img alt="NTNU logo" width="200" height="200" src="@/assets/logo.png" @click="$router.push('/about')" />
    </Row>
    <Row justify="center">
        <h2>
            電動車自動充電系統
        </h2>
    </Row>
    <div class="gap-30" />

    <Row justify="space-around">
        <Col span="12" @click="$router.push('/register')">
        <img alt="Registration" width="130" height="130" src="@/assets/Charging-station.png" />
        <h3>
            預約充電
        </h3>
        </Col>
        <Col span="12" @click="$router.push('/search')">
        <img alt="Search" width="130" height="130" src="@/assets/search.png" />
        <h3>
            查詢車輛
        </h3>
        </Col>
    </Row>

    <Row justify="center">
        <Col span="10">
        <Button round block type="primary" @click="onTest">
            Test
        </Button>
        </Col>
    </Row>
</template>

<style>
.gap-20 {
    width: 100%;
    height: 20px;
}

.gap-30 {
    width: 100%;
    height: 30px;
}

.gap-60 {
    width: 100%;
    height: 60px;
}
</style> 