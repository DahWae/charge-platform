<script setup>
import {
    Button,
    Row,
    Col,
} from 'vant'
</script>

<template>
    <Row justify="center">
        <div class="about">
            <h1>About</h1>
        </div>
    </Row>

    <Row justify="space-around">
        <Col span="8">
        <Button type='primary' to="/">Home</Button>
        </Col>
        <Col span="8" @click="$router.push('/Manager')">
        <Button type='primary'> Manager </Button>
        </Col>
    </Row>
</template>

<style>
.about {
    margin: 16px;
}
</style>
