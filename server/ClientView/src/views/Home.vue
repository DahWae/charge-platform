<script setup>
import {
    Button,
    Row,
    Col,
    Image,
    Toast,
} from 'vant'

import axios from 'axios'

const onCharge = () => {
    axios.post(robotUrl + '/action/charge',
        {
            space: 'P1'
        })
        .then(function (response) {
            console.log(response.data)
            Toast(response.data)
        })

    // axios.get(serverUrl + '/')
    //     .then(function (response) {
    //         console.log(response.data)
    //         Toast(response.data)
    //     })
};

const onReturn = () => {
    axios.post(robotUrl + '/action/return', {})
        .then(function (response) {
            console.log(response.data)
            Toast(response.data)
        })
        
    axios.get(serverUrl + '/')
        .then(function (response) {
            console.log(response.data)
            Toast(response.data)
        })
};
</script>

<template>

    <div class="gap-30" />
    <Row justify="center">
        <img class="logo" alt="NTNU logo" src="@/assets/logo.png" @click="$router.push('/manager')" />
    </Row>
    <Row justify="center">
        <h2>
            電動車自動充電系統
        </h2>
    </Row>
    <div class="gap-30" />

    <Row justify="space-around">
        <Col span="12" @click="$router.push('/register')">
        <img class="menu" alt="Registration" src="@/assets/Charging-station.png" />
        <h3>
            預約充電
        </h3>
        </Col>
        <Col span="12" @click="$router.push('/search')">
        <img class="menu" alt="Search" src="@/assets/search.png" />
        <h3>
            查詢車輛
        </h3>
        </Col>
    </Row>

    <Row justify="center">
        <Col span="10">
        <Button round block type="primary" @click="onCharge">
            Charge
        </Button>
        </Col>
    </Row>

    <Row justify="center">
        <Col span="10">
        <Button round block type="primary" @click="onReturn">
            Return
        </Button>
        </Col>
    </Row>
</template>

<style>
.logo {
    width: 150px;
    height: 150px;
}

.menu {
    width: 120px;
    height: 120px;
}

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