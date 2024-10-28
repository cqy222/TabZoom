/* eslint-disable */
<template>
  <div id="app" v-if="!loadingData">
    <el-menu
      class="el-menu-demo"
      mode="horizontal"
      background-color="#e6e6e6"
      text-color="#000"
      active-text-color="#0087d0"
    >
      <el-menu-item id="title">
        {{ appName }}
      </el-menu-item>

      <!-- <el-menu-item>
        <el-upload
          class="upload-demo"
          action="http://localhost:8080/"
          :limit="1"
          show-file-list="false"
          :on-success="handleUploadSuccess"
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :before-upload="onBeforeUpload"

        >
          <img :src="'./icon/upload.svg'" class="icon" />
        Upload Your Data
        </el-upload>
      </el-menu-item> -->

      <el-menu-item
        v-for="(operation, index) in operationArray"
        :key="operation"
        @click="changeDialogVisible(operation)"
      >
        <img :src="iconPath[index]" class="icon" />
        {{ operation }}
      </el-menu-item>
      <el-menu-item
        style="width: 15%; right: 50px !important"
        class="zoom-operator"
      >
        <el-slider
          v-model="zoomScale"
          :min="30"
          :max="150"
          :step="1"
          @input="handle_zoom_scale"
        ></el-slider>
      </el-menu-item>
      <el-menu-item class="zoom-operator" @click="handle_zoom()">
        <img :src="get_zoom_icon()" class="icon" />
      </el-menu-item>
    </el-menu>

    <!-- <div class="content-container">
      <TableView :isHeaderFixed="isHeaderFixed" @changeHeaderFixed="change_is_header_fixed($event)"></TableView> 
    </div> -->

    <div
      class="content-container"
      :class="{ 'content-container-right-margin': showVisPanel }"
    >
      <TableView :key="tableViewKey"></TableView>
    </div>

    <div
      id="vis-panel"
      :class="{
        'vis-panel-slide-in': showVisPanel,
        'vis-panel-slide-out': !showVisPanel,
      }"
      >
      <InsightView></InsightView>
    </div>

    <el-dialog
      title="Example Dataset"
      id="dataset-dialog"
      :visible.sync="datasetDialogVisible"
    >
      <DataDialog :datasetDialogKey="datasetDialogKey"> </DataDialog>
    </el-dialog>

    <el-dialog
      title="Upload"
      id="upload-dialog"
      :visible.sync="uploadDialogVisible"
    >
      <UploadDialog> </UploadDialog>
    </el-dialog>

    <el-dialog :title="dialogTitle" :visible.sync="showDialog" width="30%">
      <span>{{ dialogText }}</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="CancelDialog">No</el-button>
        <el-button type="primary" @click="ConfirmDialog">Yes</el-button>
      </span>
    </el-dialog>

    <!-- <el-dialog :title="'User Guidance'" :visible.sync="showVideo" width="1080px">
      <div style="color:red">必填！！！</div>
      <a href="https://www.wjx.cn/vj/h4Ln1n6.aspx">用户问卷调查 https://www.wjx.cn/vj/h4Ln1n6.aspx</a>
      <br>
      <br>
      <video height="540px" controls>
        <source :src="videoPath" type="video/mp4">
      </video>
    </el-dialog> -->

    <el-dialog
      title="Export"
      id="export-dialog"
      :visible.sync="exportDialogVisible"
    >
      <ExportDialog></ExportDialog>
    </el-dialog>

    <!--如果getinsight需要调用dialog那么可以在这写  -->
    <!-- <el-dialog
    title="Show Insights"
    id="showInsight-dialog"
    :visible.sync="showInsightsVisible"
    >
      <UploadDialog> </UploadDialog>
    </el-dialog>   -->

  </div>
</template>

<script>
import TableView from "./views/TableView.vue";
import InsightView from "./views/InsightView.vue";
import { getTabularDataset } from "@/communication/communicator.js";
import { parseTabularData } from "@/utils/tabularDataParser.js";
import { Dataset } from "@/dataset/dataset.js";
import DataDialog from "@/views/dialogs/DataDialog.vue";
import UploadDialog from "@/views/dialogs/UploadDialog.vue";
import ExportDialog from "@/views/dialogs/ExportDialog.vue";
import axios from 'axios'
import { mapState } from "vuex";
import VueSimpleAlert from "vue-simple-alert";
import vegaEmbed from 'vega-embed';

export default {
  name: "app",
  components: {
    InsightView,
    TableView,
    DataDialog,
    UploadDialog,
    ExportDialog,
  },
  computed: {},
  data() {
    return {
      server_address: 'http://127.0.0.1:14450',
      appName: "TabZoom",
      operationArray: ["Open Example Data", "Upload Your Data", "Export", "Show Insights"],
      iconPath: [
        "./icon/open-file.svg",
        "./icon/upload.svg",
        "./icon/save.svg",
        "./icon/insight.svg",
      ],
      // activeIndex: "",
      datasetDialogVisible: false,
      uploadDialogVisible: false,
      exportDialogVisible: false,
      showInsightsVisible: false,
      datasetDialogKey: 0,
      // insightLength: 0,
      loadingData: true,

      initializeVis: true,
      showVisPanel: true,

      showDialog: false,
      dialogTitle: "",
      dialogText: "",

      isZoomOut: false,

      zoomScale: 100,
      tableViewKey: 1,

      showVideo: true,
      videoPath:"http://r9ea0k3fo.hb-bkt.clouddn.com/guidance.mp4",
      insightID:1,
      temp_dataset_name:"Console Sales.xlsx",

      blocks_information:null ,
      singel_block_information:{Block_index:null,insight_location_header:null,insight_location4:null,insight_list:[],},
      temp_insight_location4_list: []   //存储当前数据试图需要高亮的所有block
    };
  },
  beforeMount: function () {
    let self = this;
    window.sysDatasetObj = new Dataset();
    let tabularDataDeferObj = $.Deferred();
    $.when(tabularDataDeferObj).then(function () {
      self.loadingData = false;
    });
    // let tabularDataList = ["*"];
    
    // initialize the tabular dataset
    axios({
        method: 'get',
        url: self.server_address + '/tabulardata',
        timeout: 5000
    }).then((res) => {
        console.log('tabularDatasetList', res)
        sysDatasetObj.updateTabularDatasetList(res['data']);
        tabularDataDeferObj.resolve();
    });
    
  },
  mounted: function () {
    let self = this;
    this.$bus.$on("visualize-selectedData", () => {
      this.initializeVis = true;
      this.showVisPanel = true;
    });


    this.$bus.$on("update-selected-dataset", (name) => {
      self.tableViewKey = (self.tableViewKey + 1) % 2;
      this.temp_dataset_name = name
      // 这里的逻辑可以更改，保证前后端共享一份dataset list即可
      if(this.temp_dataset_name === "Console Sales.xlsx"){
          this.insightID =1}
      if(this.temp_dataset_name === "Console Sales(cumulative).xlsx"){
          this.insightID =2}
      //更换dataset时重新获取insight
      console.log("update selected dataset"+this.insightID );
    });

    this.$bus.$on("select-canvas", () => {
      this.showVisPanel = true;
    });

    this.$bus.$on("show-dialog", (data) => {
      this.showDialog = true;
      this.dialogTitle = data.title;
      this.dialogText = data.text;
    });

    this.$bus.$on("close-data-dialog", () => {
      this.datasetDialogVisible = false;
    });

    this.$bus.$on("close-upload-dialog", () => {
      this.uploadDialogVisible = false;
    });

    this.$bus.$on("close-VisView", () => {
      // this.showVisPanel = false;
    });
    this.$bus.$on("change-zoomScale", (value) => {
      this.zoomScale = value;
    });
  },
  methods: {
    iconClass(operation) {
      return "icon-" + operation;
    },
    // closeDataDialog() {
    //   this.datasetDialogVisible = false
    // },
    changeDialogVisible(panel_name) {
      console.log("panel_name", panel_name);
      if (panel_name === "Open Example Data") {
        this.datasetDialogVisible = true;
      }
      if (panel_name === "Upload Your Data") {
        this.uploadDialogVisible = true;
      }
      if (panel_name === "Export") {
        this.exportDialogVisible = true;
      }
      if (panel_name === "Show Insights") {
        this.showInsightsVisible = true;
        // 当点击getinsight图标时，像后端请求获取所有block_insights
        axios({
          method: 'post',  
          url: this.server_address + '/getblockinsight',
          timeout: 5000,
          data: {
              file_id: this.insightID  // 传递 file_id 参数
          }
          }).then((res) => {
              console.log('blocks_information:', res.data);  // Accessing data from response
              this.blocks_information = res.data;  // Ensure the context is correct
              // this.$alert(this.blocks_information);
              // 提取每个块的insight_location4数据并存入数组
              this.temp_insight_location4_list = this.blocks_information.map(block => block.insight_location4);
              // this.$alert(this.temp_insight_location4_list);
              this.$bus.$emit("pass_blocks_information", this.blocks_information); 
              this.$bus.$emit("show_block_insight_information", this.temp_insight_location4_list); 
          }).catch((error) => {
              console.error('Error fetching block_insights:', error);
        }); 
      }
    },
    ConfirmDialog() {
      this.showDialog = false;
      this.$bus.$emit("confirm-dialog", this.dialogText);
    },
    CancelDialog() {
      this.showDialog = false;
      this.$bus.$emit("cancel-dialog", this.dialogText);
    },
    get_zoom_icon() {
      if (this.isZoomOut) {
        return "./icon/resume.svg";
      } else return "./icon/fitin.svg";
    },
    handle_zoom() {
      this.isZoomOut = !this.isZoomOut;
      this.$bus.$emit("change-zoom");
    },
    handle_zoom_scale(value) {
      this.$bus.$emit("change-zoom", value);
    },
  },
};
</script>

<style lang="less">
@side-panel-width: 20%;
@padding: 0.7rem;
@menu-height: 2.5rem;
@icon-size: 1.4rem;

html {
  font-size: 100%;
}
.zoom-operator {
  position: absolute !important;
  right: 10px !important;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  position: absolute;
  top: 0%;
  bottom: 0%;
  left: 0%;
  right: 0%;
  overflow: hidden;
  .el-menu.el-menu--horizontal {
    border-bottom: none;
    .el-menu-item {
      height: @menu-height;
      line-height: @menu-height;
      font-size: 90%;
      padding: 0 10px;
      .icon {
        width: @icon-size;
        height: @icon-size;
      }
    }
    #title {
      font-weight: bolder;
      font-size: 115%;
    }
  }
  .el-slider__runway {
    background-color: white !important;
  }
  .vis-panel-slide-in {
    animation: slide-in 0.3s cubic-bezier(0.36, 0.07, 0.19, 0.97);
    transform: translateX(0);
  }
  .vis-panel-slide-out {
    animation: slide-out 0.3s cubic-bezier(0.36, 0.07, 0.19, 0.97);
    transform: translateX(100%);
    transition-delay: display 2s;
  }
  @keyframes slide-out {
    from {
      transform: translateX(0);
    }
    to {
      transform: translateX(100%);
    }
  }

  .content-container-right-margin {
    transition-delay: 0.3s;
    right: @side-panel-width !important;
  }

  @keyframes slide-in {
    from {
      transform: translateX(100%);
    }
    to {
      transform: translateX(0);
    }
  }
  .content-container {
    position: absolute;
    top: @menu-height;
    left: 0;
    bottom: 0;
    right: 0;
    margin-right: @padding;
  }
  svg:not(:root) {
    overflow: visible;
  }
  #vis-panel {
    position: absolute;
    right: 0%;
    width: @side-panel-width;
    top: @menu-height;
    bottom: 0%;
    border-left: solid #efefef 1px;
    background-color: white;
  }

  // scroll bar
  ::-webkit-scrollbar {
    width: 5px;
    height: 5px;
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb {
    background-color: #dcdfe6;
    border-radius: 5px;
    // visibility: hidden;
    &:hover {
      visibility: visible;
    }
  }
}
</style>
