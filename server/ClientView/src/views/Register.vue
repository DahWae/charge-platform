<script setup>
import {
    ref
} from 'vue'


import {
    Row,
    Col,
    Form,
    Field,
    CellGroup,
    Button,
    Popup,
    DatetimePicker,
    Slider,
    ConfigProvider,
    Toast,
} from 'vant'

import axios from 'axios'

const plate = ref('');
const parkID = ref('');
const power = ref('');
const time = ref('');
const showPicker = ref(false);

const value = ref(100);
const onChange = (value) => Toast('當前值：' + value / 10);

const onConfirm = (value) => {
    time.value = value;
    showPicker.value = false;
};

const onSubmit = (values) => {
    axios.post(serverUrl + '/submit', values)
        .then(function (response) {
            console.log(response)
            Toast(response.statusText)
        })
        .catch(function (error) {
            console.log(error)
            Toast('ERROR')
        })
};


</script>


<template>
    <Row justify="center">
        <Form @submit="onSubmit">

            <CellGroup inset>
                <Field v-model="plate" name="Plate" label="車牌號碼" placeholder="ABC-1234"
                    :rules="[{ required: true, message: '請填寫車牌' }]" />
            </CellGroup>

            <CellGroup inset>
                <Field v-model="parkID" name="ParkID" label="停車格位置" placeholder="A-1"
                    :rules="[{ required: true, message: '請填寫停車格位置' }]" />
            </CellGroup>



            <CellGroup inset>
                <Col span="24">
                <field v-model="power" name="Power" label="充電度數">
                    <template #input>
                        <slider v-model="value" max="200" @change="onChange" style="bar-height: 20px;" />

                        <div> {{ value / 10 }} </div>
                    </template>
                </field>
                </Col>
            </CellGroup>

            <CellGroup inset>
                <Field v-model="time" is-link readonly name="PickTime" label="取車時間" placeholder="請選擇時間"
                    @click="showPicker = true;" :rules="[{ required: true, message: '請填寫取車時間' }]" />
                <Popup v-model:show="showPicker" position="bottom" style="{height:30px}">
                    <DatetimePicker type="time" title="請選擇取車時間" confirm-button-text="確認" cancel-button-text="取消"
                        @confirm="onConfirm" @cancel="showPicker = false" />
                </Popup>
            </CellGroup>

            <CellGroup>
                <div class="gap">
                    <Button round block type="primary" native-type="submit">
                        送出
                    </Button>
                </div>
            </CellGroup>
        </Form>
    </Row>

</template>

<style>
.gap {
    margin: 16px;
}
</style>