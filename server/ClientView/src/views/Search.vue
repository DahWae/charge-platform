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
} from 'vant'
import router from '@/router';

const plate = ref('');

const onSubmit = (values) => {
    console.log('submit', values);
    router.push({ name: 'Result', query: {plate: plate.value} });
};

</script>


<template>
    <Row justify="center">
        <Form @submit="onSubmit">

            <CellGroup inset>
                <Field v-model="plate" name="Plate" label="車牌號碼" placeholder="ABC-1234"
                    :rules="[{ required: true, message: '請填寫車牌' }]" />
            </CellGroup>

            <CellGroup>
                <div class="gap">
                    <Button round block type="primary" native-type="submit">
                        搜尋車輛
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