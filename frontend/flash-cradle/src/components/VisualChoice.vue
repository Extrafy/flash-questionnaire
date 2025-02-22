<template scope="this api replaced by slot-scope in 2.5.0+">
    <div>
        <div style="width: 100%; height: 50px; background-color: rgb(238, 244, 251); border: 3px solid rgb(238, 244, 251);">
            <div style=" width: calc(100% - 130px); display: inline-block; "></div>
            <el-select v-model="value" placeholder="选择样式" style="font-family: Arial; display: inline-block; width: 120px; margin-top: 10px;">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"/>
            </el-select>
        </div>
        <div ref="container" :style="{ display: dis }" style="width:100%; height: calc(100% - 50px); border: 3px solid rgb(238, 244, 251);"></div>
    </div>
</template>

<script>
import { ElSelect, ElOption } from "element-plus"
export default {
    name: "VisualChoice",
    components: {
        ElSelect, ElOption
    },
    props: {
        data: Array
    },
    data() {
        return {
            value: '收起',
            type: 'column',
            innerSize: '0%',
            dis: "none",
            options: [
                { type: 'line', value: '折线图', },
                { type: 'column', value: '柱状图', },
                { type: 'pie', value: '饼状图', innerSize: '0%'},
                { type: 'pie', value: '环状图', innerSize: '70%'},
                { type: 'none', value: '收起'}
            ]
        };
    },
    watch: {
        value(newVal) {
            this.type = this.options.find(option => option.value === newVal).type;
            if (this.type === 'pie')
                this.innerSize = this.options.find(option => option.value === newVal).innerSize;
            if (this.type !== 'none') {
                this.dis = "block";
                this.createContainer();
            }
            else
                this.dis = "none";
        }
    },
    mounted() {
        this.createContainer()
    },
    methods: {
        createContainer() {
            var Highcharts = require('highcharts');
            require('highcharts/modules/exporting')(Highcharts);
            Highcharts.chart(this.$refs.container, {
                chart: {
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false,
                    type: this.type
                },
                title: {
                    text: ' ',
                    visible: false
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        formatter: function() {
                            return this.value;
                        }
                    }
                },
                yAxis: {
                    title: {
                        text: '',
                        visible: false
                    }
                },
                tooltip: {
                    enabled: false
                },
                plotOptions: {
                    pie: {
                        allowPointSelect: false,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return '<span>' + this.point.name + '</span>: <b>' + this.y + '</b>';
                            }
                        },
                        showInLegend: true,
                        innerSize: this.innerSize
                    },
                    column: { 
                        allowPointSelect: false,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return this.y;
                            }
                        }
                    },
                    line: {
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels: {
                            enabled: true,
                            formatter: function() {
                                return this.y;
                            }
                        }
                    }
                },
                legend: {
                    enabled: false
                },
                series: [{
                    name: '选项',
                    colorByPoint: true,
                    data: this.data
                }]
            
            });
        }
    },
    
}
</script>

<style scoped>

</style>