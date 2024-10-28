<template>
    <div v-if="vega.length > 0" class="insight-view">
      <div class="panel-header">
        <h2>Insights</h2>
      </div>
      <!-- 图表列表容器 -->
      <div class="chart-container">
        <div v-for="(spec, index) in vega" :key="index" ref="chartRefs" class="vega-chart-wrapper">
          <div class="vega-chart"></div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import vegaEmbed from 'vega-embed';
  
  export default {
    name: 'InsightView',
    data() {
      return {
        vega: []  // 初始化为空数组，将通过事件监听填充
      };
    },
    mounted() {
      this.$bus.$on('show_selectedInsights', this.updateCharts);
    },
    beforeDestroy() {
      this.$bus.$off('show_selectedInsights', this.updateCharts);
    },
    methods: {
      updateCharts(vegaSpecs) {
        // 创建 vegaSpecs 的深拷贝
        this.vega = vegaSpecs.map(spec => JSON.parse(JSON.stringify(spec)));
        this.$nextTick(this.renderAllCharts);
      },
      renderAllCharts() {
        this.$refs.chartRefs.forEach((el, index) => {
        const specCopy = JSON.parse(JSON.stringify(this.vega[index]));
          vegaEmbed(el.children[0], specCopy, { "actions": false })
            .then((result) => console.log("Chart was embedded successfully!"))
            .catch(console.error);
        });
      }
    }
  };
  </script>
  
  <style>
  .insight-view {
    position: fixed;  /* 或absolute, 根据需要定位 */
    right: 0;  /* 定位到右侧 */
    top: 0;  /* 从顶部开始 */
    height: 100%;  /* 全屏高度 */
    width: 100%;  /* 宽度调整为屏幕的30% */
    overflow-y: auto; /* 允许垂直滚动 */
    background-color: #f7f7f7;  /* 浅灰色背景 */
    border-left: 1px solid #ccc;  /* 左边界 */
    box-shadow: -5px 0 15px rgba(0,0,0,0.1);  /* 向左的阴影 */
  }
  
  .panel-header {
    padding: 16px;
    background-color: #ffffff; /* 白色背景 */
    border-bottom: 1px solid #eee; /* 底部边框 */
    text-align: center;
  }
  
  .vega-chart-wrapper {
    margin: 10px;
    padding: 10px;
    background-color: #ffffff; /* 每个图表的背景为白色 */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* 轻微阴影效果 */
    border-radius: 8px; /* 圆角边框 */
  }
  
  .vega-chart {
    width: 100%;  /* 确保图表宽度充满容器 */
    height: 400px; /* 每个图表的高度 */
  }
  </style>
  