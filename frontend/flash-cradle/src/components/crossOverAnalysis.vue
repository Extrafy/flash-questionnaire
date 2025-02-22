<template>
  <div>
    <figure class="highcharts-figure">
      <div
        style="
          width: 100%;
          height: 50px;
          background-color: white;
          background-color: rgb(238, 244, 251);
        "
      >
        <div
          style="
            font-size: 20px;
            display: inline-block;
            width: 160px;
            margin-top: 10px;
            margin-left: 10px;
            font-family: Arial;
          "
        >
          交叉分析图
        </div>
        <div style="width: calc(100% - 300px); display: inline-block"></div>
        <el-select
          v-model="selectedOption"
          placeholder="选择样式"
          style="font-family: Arial; display: inline-block; width: 120px"
          @change="updateChartType"
        >
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div id="container" ref="chartContainer"></div>
      <p>
        <strong style="margin-right: 636px">自变量X</strong>
        <strong>因变量Y</strong>
      </p>
    </figure>

    <div id="controls">
      <select v-model="selectedCategory">
        <option
          v-for="category in categories"
          :key="category"
          :value="category"
        >
          {{ category.text }}
        </option>
      </select>
      <select v-model="selectedYears">
        <option v-for="year in years" :key="year" :value="year">
          {{ year.text }}
        </option>
      </select>
    </div>
    <div id="controls">
      <el-button type="primary" @click="renderChart">交叉分析</el-button>
    </div>
  </div>
</template>

<script>
import { ref, watch } from "vue";
import Highcharts from "highcharts";
import exportingInit from "highcharts/modules/exporting";
import exportDataInit from "highcharts/modules/export-data";
import accessibilityInit from "highcharts/modules/accessibility";
import "element-plus/dist/index.css";
import { ElSelect, ElOption, ElButton } from "element-plus";
import { useRoute } from "vue-router";
import { getapi2 } from "../../api/account/crossAnalysis";
// Initialize the Highcharts modules
exportingInit(Highcharts);
exportDataInit(Highcharts);
accessibilityInit(Highcharts);

export default {
  name: "HighchartsComponent",
  components: {
    ElSelect,
    ElOption,
    ElButton,
  },
  props: {
    categories: {
      type: Array,
      required: true,
    },
    years: {
      type: Array,
      required: true,
    },
  },
  setup() {
    const chartContainer = ref(null);
    const chart = ref(null);
    const isChartRendered = ref(false);

    const selectedCategory = ref(null);
    const selectedYears = ref(null);
    const selectedOption = ref("柱状图");

    const route = useRoute();
    const q_id = route.query.q_id;
    console.log(q_id);
    const q_name = route.query.q_name;
    console.log(q_name);
    const chartData = ref(null);
    const options = [
      { type: "line", value: "折线图", label: "折线图" },
      { type: "column", value: "柱状图", label: "柱状图" },
      { type: "bar", value: "条形图", label: "条形图" },
    ];

    const renderChart = async () => {
      if (!chartContainer.value) return;
      if (selectedCategory.value == null || selectedYears.value == null) {
        alert("请选择题目");
        return;
      }
      if (selectedCategory.value.value == selectedYears.value.value) {
        alert("题目不能重复");
        return;
      }

      const data = {
        qn_id: parseInt(q_id),
        q_id1: parseInt(selectedYears.value.id),
        q_id2: parseInt(selectedCategory.value.id),
      };
      try {
        const response = await getapi2(data);
        console.log("尝试获取2成功:", response.data);

        chartData.value = {
          overTime: {
            recent: {
              categories: response.data.list[0].q2_options.map(
                (option) => option.content
              ),
              series: response.data.list[1].count
                .filter((count) => count.content !== 0)
                .map((count) => ({
                  name: count.content,
                  data: count.options.map((option) => option.count),
                })),
            },
          },
        };

        console.log(JSON.stringify(chartData.value, null, 2));
      } catch (error) {
        console.error("尝试失败:", error);
      }

      const dataPath = chartData.value.overTime.recent;
      if (!dataPath) {
        alert("无数据可显示");
        return;
      }

      chart.value = Highcharts.chart(chartContainer.value, {
        chart: {
          type: options.find((opt) => opt.value === selectedOption.value)?.type,
        },
        title: {
          text: q_name,
        },
        legend: {
          align: "right",
          verticalAlign: "middle",
          layout: "vertical",
        },
        xAxis: {
          categories: dataPath.categories,
          labels: {
            x: -10,
          },
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Amount",
          },
        },
        series: dataPath.series,
        responsive: {
          rules: [
            {
              condition: {
                maxWidth: 500,
              },
              chartOptions: {
                legend: {
                  align: "center",
                  verticalAlign: "bottom",
                  layout: "horizontal",
                },
                yAxis: {
                  labels: {
                    align: "left",
                    x: 0,
                    y: -5,
                  },
                  title: {
                    text: null,
                  },
                },
                subtitle: {
                  text: null,
                },
                credits: {
                  enabled: false,
                },
              },
            },
          ],
        },
      });
      chart.value.viewData();
      isChartRendered.value = true;
    };

    const updateChart = () => {
      if (!isChartRendered.value || !chart.value) return;

      const dataPath = chartData.value.overTime.recent;

      while (chart.value.series.length) {
        chart.value.series[0].remove(false);
      }

      dataPath.series.forEach((serie) => {
        chart.value.addSeries(serie, false);
      });

      chart.value.update(
        {
          chart: {
            type: options.find((opt) => opt.value === selectedOption.value)
              ?.type,
          },
          xAxis: {
            categories: dataPath.categories,
          },
        },
        true
      );
    };

    const updateChartType = () => {
      if (!isChartRendered.value || !chart.value) return;

      const option = options.find((opt) => opt.value === selectedOption.value);
      if (option) {
        chart.value.update({
          chart: {
            type: option.type,
          },
        });
      }
    };

    watch(selectedOption, () => {
      updateChartType();
    });

    return {
      chartContainer,
      selectedCategory,
      selectedYears,
      updateChart,
      selectedOption,
      options,
      updateChartType,
      renderChart,
    };
  },
};
</script>

<style>
.highcharts-figure,
.highcharts-data-table table {
  min-width: 310px;
  max-width: 800px;
  margin: 1em auto;
}

.highcharts-data-table table {
  font-family: Verdana, sans-serif;
  border-collapse: collapse;
  border: 1px solid #ebebeb;
  margin: 10px auto;
  text-align: center;
  width: 100%;
  max-width: 500px;
}

.highcharts-data-table caption {
  padding: 1em 0;
  font-size: 1.2em;
  color: #555;
}

.highcharts-data-table th {
  font-weight: 600;
  padding: 0.5em;
}

.highcharts-data-table td,
.highcharts-data-table th,
.highcharts-data-table caption {
  padding: 0.5em;
}

.highcharts-data-table thead tr,
.highcharts-data-table tr:nth-child(even) {
  background: #f8f8f8;
}

.highcharts-data-table tr:hover {
  background: #f1f7ff;
}

#button-bar,
#controls {
  min-width: 310px;
  max-width: 800px;
  margin: 0 auto;
}

#controls {
  margin-bottom: 1em;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#controls select {
  padding: 0.5em;
  font-size: 1em;
}
</style>
