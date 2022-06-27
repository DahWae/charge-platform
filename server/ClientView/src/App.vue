<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import {
  NavBar,
  Row,
  Col,
  Icon,
} from 'vant'
</script>

<template>
  <NavBar title="自動充電系統">
    <template #left>
      <Icon size="2rem" name="wap-home" @click="$router.push('/')" />
    </template>
  </NavBar>

  <div class="gap-30" />

  <router-view />

  <Row class="footer" jusitfy="center" align="bottom">
    <Col span="24">
    <body style="font-size:xx-small">Powered by<br />國立臺灣師範大學 電機控制與應用實驗室</body>
    </Col>
  </Row>
</template>

<style>
@font-face {
  font-family: 'Noto Sans TC';
  src: url(@/assets/font/NotoSansTC-Regular.otf);
}

#app {
  font-family: 'Noto Sans TC', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}

.gap-10 {
  width: 100%;
  height: 10px;
}

.gap-20 {
  width: 100%;
  height: 20px;
}

.gap-30 {
  width: 100%;
  height: 30px;
}

.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
}
</style>
