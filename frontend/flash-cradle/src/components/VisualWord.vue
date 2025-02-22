<template scope="this api replaced by slot-scope in 2.5.0+">
    <div>
        <div style="width: 100%; height: 50px; background-color: rgb(238, 244, 251); ">
            <div style=" width: calc(100% - 130px); display: inline-block; "></div>
            <el-select v-model="value" placeholder="选择样式" style="font-family: Arial; display: inline-block; width: 120px; margin-top: 10px;">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"/>
            </el-select>
        </div>
        <div ref="container" :style="{ display: type }" style="border: 3px solid rgb(238, 244, 251);"></div>
    </div>
</template>

<script scope>
import Highcharts from 'highcharts';    
import HC_exporting from 'highcharts/modules/exporting';  
import wordcloud from 'highcharts/modules/wordcloud';
import { ElSelect, ElOption } from "element-plus"

export default {
    name: "VisualWord",
    components: {
        ElSelect, ElOption
    },
    props: {
        txt: Array
    },
    data() {
        return {
            value: '收起',
            type: 'none',
            options: [
                { type: 'block', value: '展示', },
                { type: 'none', value: '收起', }
            ]
        }
    },
    watch: {
        value(newVal) {
            this.type = this.options.find(option => option.value === newVal).type;
            if (this.type === 'block')
                this.createCloud();
        },
    },
    methods: {
        createCloud() {
            HC_exporting(Highcharts); 
            wordcloud(Highcharts);
            var data = this.txt.map(item => ({
                name: item.name,
                weight: item.y
            })).sort(function(a, b) { return b.weight - a.weight; });
            Highcharts.chart(this.$refs.container, {
                series: [{
                    type: 'wordcloud',
                    data: data
                }],
                title: {
                    text: '',
                    align: 'left'
                }
            });
        }
    },
}
</script>

<style scoped>
.bt {
    width: 120px;
    margin-top: 10px;
    font-size: 15px;
    height: 30px;
    border-radius: 5px;
    background-color: #007bff;
    border: 0px;
    color: white;
}
.bt:hover {
    background-color: #0056b3;
    cursor:pointer;
}
</style>