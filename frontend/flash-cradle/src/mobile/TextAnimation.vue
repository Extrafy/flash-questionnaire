<template>
  <span class="container">
    <input type="text" :style="{ fontSize: fSize, color: fColor }" :value="text" readonly class="input-field">
  </span>
</template>

<script>

export default {
  name: "TextAnimation",
  props: {
    dText: {
      type: Array,
      default: () => ["调查问卷", "考试试卷", "报名表", "接龙问卷"]
    },
    fontSize: {
      type: String,
      default:() => "100px"
    },
    fontColor: {
      type: String,
      default:() => "black"
    }
  },
  data() {
    return {
      dynamicText: this.dText.slice(),
      fSize: this.fontSize,
      fColor: this.fontColor,
      text: "",
      index: 0,
      direction: 1,
      showpointer: 1,
      interval: 0,
      currentIndex: 0,
      intervalId: null
    };
  },
  mounted() {
    this.text = "";
    this.intervalId = setInterval(this.updateText, 100);
  },
  methods: {
    updateText() {
      if (this.interval >= 0) {
        this.interval -= 1;
        return;
      }
      if (this.showpointer === 3) {
          this.text += '｜';
          this.showpointer = 0;
      }
      else {
        if (this.showpointer === 0) {
          this.text = this.text.slice(0, -1);
        }
        this.showpointer += 1;
        if (this.direction === 1) {
          if (this.index < this.dynamicText[this.currentIndex].length) {
            this.text += this.dynamicText[this.currentIndex][this.index];
            this.index++;
          } else {
            this.direction = -1;
            this.interval = 6;
          }
        } else {
          if (this.index > 0) {
            this.text = this.text.slice(0, -1);
            this.index--;
          } else {
            this.interval = 1;
            this.direction = 1;
            this.currentIndex = (this.currentIndex + 1) % (this.dynamicText.length);
          }
        }
      }
      
    }
  },
  beforeUnmount() {
    clearInterval(this.intervalId);
  }
};
</script>

<style scoped>
.container {
  background-color: transparent;
  max-width: 400px;
}
.input-field {
  border: none;
  outline: none;
  max-width: 500px;
  max-height: 105px;
  background-color: transparent;
  font-family: Arial, Helvetica, sans-serif;
}
</style>
