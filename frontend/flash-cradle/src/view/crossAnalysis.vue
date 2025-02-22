<template>
  <div v-if="loading">Loading...</div>
  <div
    style="
      position: absolute;
      width: 100%;
      height: 100%;
      background: rgb(249, 251, 255);
      min-width: 800px;
      overflow-y: scroll;
    "
    v-else
  >
    <ConsoleHeader></ConsoleHeader>
    <crossOverAnalysis
      :chartData="chartData"
      :categories="categories"
      :years="years"
      style="margin-top: 90px"
    />
  </div>
</template>

<script>
import crossOverAnalysis from "@/components/crossOverAnalysis.vue";
import ConsoleHeader from "../components/ConsoleHeader.vue";

export default {
  components: {
    crossOverAnalysis,
    ConsoleHeader,
  },
  data() {
    return {
      // chartData: {
      //   recent: {
      //     allTime: {
      //       categories: [
      //         "2015",
      //         "2016",
      //         "2017",
      //         "2018",
      //         "2019",
      //         "2020",
      //         "2021",
      //       ],
      //       series: [
      //         {
      //           name: "2019",
      //           data: [29, 30, 35, 40, 38, 51, 34],
      //         },
      //         {
      //           name: "2020",
      //           data: [25, 28, 30, 29, 31, 26, 27],
      //         },
      //         {
      //           name: "2021",
      //           data: [34, 36, 39, 41, 38, 42, 41],
      //         },
      //       ],
      //     },
      //     overTime: {
      //       categories: ["2017", "2018", "2019", "2020", "2021"],
      //       series: [
      //         {
      //           name: "2019",
      //           data: [35, 40, 38, 51, 34],
      //         },
      //         {
      //           name: "2020",
      //           data: [30, 29, 31, 26, 27],
      //         },
      //         {
      //           name: "2021",
      //           data: [39, 41, 38, 42, 41],
      //         },
      //       ],
      //     },
      //   },
      //   allTime: {
      //     recent: {
      //       categories: ["2019", "2020", "2021"],
      //       series: [
      //         {
      //           name: "2015",
      //           data: [45, 50, 55],
      //         },
      //         {
      //           name: "2016",
      //           data: [40, 45, 50],
      //         },
      //         {
      //           name: "2017",
      //           data: [45, 50, 55],
      //         },
      //         {
      //           name: "2018",
      //           data: [40, 45, 50],
      //         },
      //         {
      //           name: "2019",
      //           data: [45, 50, 55],
      //         },
      //         {
      //           name: "2020",
      //           data: [40, 45, 50],
      //         },
      //         {
      //           name: "2021",
      //           data: [40, 45, 50],
      //         },
      //       ],
      //     },

      //     overTime: {
      //       categories: ["2017", "2018", "2019", "2020", "2021"],
      //       series: [
      //         {
      //           name: "2015",
      //           data: [35, 40, 38, 51, 34],
      //         },
      //         {
      //           name: "2016",
      //           data: [30, 29, 31, 26, 27],
      //         },
      //         {
      //           name: "2017",
      //           data: [35, 40, 38, 51, 34],
      //         },
      //         {
      //           name: "2018",
      //           data: [30, 29, 31, 26, 27],
      //         },
      //         {
      //           name: "2019",
      //           data: [35, 40, 38, 51, 34],
      //         },
      //         {
      //           name: "2020",
      //           data: [30, 29, 31, 26, 27],
      //         },
      //         {
      //           name: "2021",
      //           data: [35, 40, 38, 51, 34],
      //         },
      //       ],
      //     },
      //   },
      //   overTime: {
      //     recent: {
      //       categories: ["2019", "2020", "2021"],
      //       series: [
      //         {
      //           name: "2017",
      //           data: [38, 51, 34],
      //         },
      //         {
      //           name: "2018",
      //           data: [31, 26, 27],
      //         },
      //         {
      //           name: "2019",
      //           data: [38, 42, 41],
      //         },
      //         {
      //           name: "2020",
      //           data: [100, 42, 23],
      //         },
      //         {
      //           name: "2021",
      //           data: [56, 32, 23],
      //         },
      //       ],
      //     },
      //     allTime: {
      //       categories: [
      //         "2015",
      //         "2016",
      //         "2017",
      //         "2018",
      //         "2019",
      //         "2020",
      //         "2021",
      //       ],
      //       series: [
      //         {
      //           name: "2017",
      //           data: [29, 43, 35, 85, 38, 51, 34],
      //         },
      //         {
      //           name: "2018",
      //           data: [29, 30, 35, 40, 38, 51, 34],
      //         },
      //         {
      //           name: "2019",
      //           data: [29, 30, 24, 40, 21, 51, 42],
      //         },
      //         {
      //           name: "2020",
      //           data: [25, 28, 30, 29, 31, 26, 27],
      //         },
      //         {
      //           name: "2021",
      //           data: [34, 36, 39, 41, 38, 42, 41],
      //         },
      //       ],
      //     },
      //   },
      // },
    };
  },
};
</script>

<script setup>
import { useRoute } from "vue-router";
import { getapi1 } from "../../api/account/crossAnalysis";
import { ref, onMounted } from "vue";

const route = useRoute();
const q_id = route.query.q_id;
console.log(q_id);

const loading = ref(true);
const categories = ref([]);
const years = ref([]);

console.log(categories);
console.log(years);

onMounted(async () => {
  console.log("尝试获取1");
  console.log("q_id:", q_id);
  const data = { qn_id: parseInt(q_id) };

  try {
    const response = await getapi1(data);
    console.log("尝试获取1成功:", response.data);
    console.log(response.data.list);
    categories.value = response.data.list.map((item) => ({
      value: item.title,
      text: item.title,
      id: item.id,
    }));
    years.value = response.data.list.map((item) => ({
      value: item.title,
      text: item.title,
      id: item.id,
    }));
    console.log(categories.value);
    console.log(years.value);
  } catch (error) {
    console.error("1失败:", error);
  } finally {
    loading.value = false;
  }
});
</script>
