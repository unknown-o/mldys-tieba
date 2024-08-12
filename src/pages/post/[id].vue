<template>
  <v-container style="max-width: 800px">
    <v-row dense style="margin: 0px 20px">
      <router-link :to="{ path: '/' }">
        <h1 class="text-primary" style="margin: 15px 0px">
          <v-btn variant="text" icon="mdi-arrow-left"> </v-btn>
          {{ isSuccess ? postData.title : "迷路的牙刷" }}
        </h1>
      </router-link>
    </v-row>
    <div v-if="loading.show" style="text-align: center; margin: 15vh">
      <v-progress-circular :size="50" color="amber" indeterminate></v-progress-circular>
      <div style="margin-top: 15px">{{ loading.message }}</div>
    </div>
    <div v-else-if="error.show" style="text-align: center; margin: 15vh">
      <v-icon size="50" color="red">mdi-close-circle</v-icon>
      <div style="margin-top: 15px">{{ error.message }}</div>
    </div>
    <div v-else>
      <v-tabs v-model="tab" bg-color="primary" style="margin: 20px">
        <v-tab value="one">文字版</v-tab>
        <v-tab value="two">原帖截图</v-tab>
        <v-tab value="three">原帖地址</v-tab>
      </v-tabs>

      <v-tabs-window v-model="tab">
        <v-tabs-window-item value="one" style="padding: 20px">
          <div v-for="item in postData.content">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                :elevation="isHovering ? 12 : 1"
                v-bind="props"
                class="mb-2"
                style="padding-top: 10px"
              >
                <v-card-title>{{ item.nickname }}</v-card-title>
                <v-card-subtitle
                  >{{ item.floor_num == 1 ? "主题帖" : `${item.floor_num}` }} 发布于{{
                    item.created_at
                  }}
                </v-card-subtitle>
                <v-card-text>{{
                  item.content
                    ? item.content
                    : "此板可能为图片或者其他多媒体内容，暂时无法显示"
                }}</v-card-text>
                <div v-if="item.reply_list.length != 0" style="margin: 3px">
                  <div style="margin-left: 30%">
                    <v-divider class="my-4 justify"></v-divider>
                    <div style="margin-bottom: 10px">回复列表：</div>
                    <v-card v-for="item1 in item.reply_list" v-bind="props" class="mb-2">
                      <v-card-text
                        >{{ item1.nickname }}:
                        {{
                          item1.content
                            ? item1.content
                            : "此板可能为图片或者其他多媒体内容，暂时无法显示"
                        }}</v-card-text
                      >
                    </v-card>
                  </div>
                </div>
              </v-card>
            </v-hover>
          </div>
        </v-tabs-window-item>
        <v-tabs-window-item value="two" style="padding: 20px">
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              :elevation="isHovering ? 12 : 1"
              v-bind="props"
              class="mb-2"
              style="padding-top: 10px"
            >
              <a
                target="_blank"
                :href="`https://static-1.llilii.cn/mldys/${postId}/screenshot.png`"
              >
                <v-img
                  v-bind:src="`https://static-1.llilii.cn/mldys/${postId}/screenshot.png`"
                >
                </v-img>
              </a>
            </v-card>
          </v-hover>
        </v-tabs-window-item>
        <v-tabs-window-item value="three" style="padding: 20px">
          <a :href="`https://tieba.baidu.com/p/${postId}`" target="_blank"
            >https://tieba.baidu.com/p/{{ postId }}</a
          >
        </v-tabs-window-item>
      </v-tabs-window>
    </div>
  </v-container>
</template>
<script setup>
import { ref, reactive, watch } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();
const postId = route.params.id;
let tab = ref("one");
let loading = reactive({
  show: true,
  message: "正在加载元数据",
});
let error = reactive({
  show: false,
  message: "呜呜呜，信息获取失败了",
});
let isSuccess = ref(false);
let postData = ref({});

const getPostData = () => {
  loading.message = "加载帖子中...";
  loading.show = true;
  fetch(`https://static-1.llilii.cn/mldys/${postId}/post-data.json`)
    .then((response) => response.json())
    .then((data) => {
      loading.show = false;
      postData.value = data;
      isSuccess.value = true;
      document.title = data.title;
    })
    .catch((err) => {
      loading.show = false;
      error.show = true;
      error.message = "呜呜呜，加载帖子出错了";
    });
};
getPostData();
</script>
