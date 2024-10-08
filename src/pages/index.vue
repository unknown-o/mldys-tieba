<template>
  <v-container>
    <v-row dense>
      <v-col cols="12" xs="12" sm="6" md="5" lg="5" offset-lg="1">
        <h1 class="my-6 ml-1 justify text-primary">迷路的牙刷</h1>
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="12" xs="12" sm="4" lg="3" offset-lg="1">
        <v-hover v-slot="{ isHovering, props }">
          <v-card :elevation="isHovering ? 12 : 1" v-bind="props" class="mb-2">
            <v-card-text>
              <div class="ma-3 justify">
                <h2>公告</h2>
                <v-divider class="my-4 justify"></v-divider>
                <p v-html="announcement"></p>
              </div>
            </v-card-text>
          </v-card>
        </v-hover>
        <v-hover v-slot="{ isHovering, props }">
          <v-card :elevation="isHovering ? 12 : 1" v-bind="props" class="mb-2">
            <v-card-text>
              <div class="ma-3 justify">
                <h2>搜索</h2>
                <v-divider class="my-4 justify"></v-divider>
                <v-select
                  label="搜索方式"
                  :items="['用户昵称', '帖子主题', '帖子内容']"
                  v-model="filter.type"
                ></v-select>
                <v-text-field
                  :label="`${filter.type}`"
                  v-model="filter.keyword"
                  required
                ></v-text-field>

                <v-card-actions class="justify-end">
                  <v-btn @click="readomData" variant="text">打乱帖子</v-btn>
                </v-card-actions>
              </div>
            </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
      <v-col cols="12" xs="12" sm="8" lg="7">
        <div v-if="loading.show" style="text-align: center; margin: 15vh">
          <v-progress-circular
            :size="50"
            color="#9932CC"
            indeterminate
          ></v-progress-circular>
          <div style="margin-top: 15px">{{ loading.message }}</div>
        </div>
        <div v-else-if="error.show" style="text-align: center; margin: 15vh">
          <v-icon size="50" color="red">mdi-close-circle</v-icon>
          <div style="margin-top: 15px">{{ error.message }}</div>
        </div>
        <div v-else>
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              :elevation="isHovering ? 12 : 1"
              v-bind="props"
              class="mb-2"
              style="padding-top: 10px"
            >
              <v-pagination
                v-model="filter.page"
                :length="Math.ceil(filteredTotal / filter.size)"
                :total-visible="5"
                style="margin-bottom: 10px"
              ></v-pagination>
            </v-card>
          </v-hover>

          <div v-for="item in displayList">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                :elevation="isHovering ? 12 : 1"
                v-bind="props"
                class="mb-2"
                style="padding-top: 10px"
              >
                <v-card-title>{{ item.title }}</v-card-title>
                <v-card-subtitle
                  >{{ item.floor_num == 1 ? "主题帖" : `${item.floor_num}` }} 发布于{{
                    item.created_at
                  }}
                  来自{{ item.nickname }}</v-card-subtitle
                >
                <v-card-text>{{ item.content }}</v-card-text>
                <v-card-actions class="justify-end">
                  <router-link :to="{ path: `/post/${item.post_id}` }"
                    ><v-btn style="color: black">查看完整帖子</v-btn>
                  </router-link>
                </v-card-actions>
              </v-card>
            </v-hover>
          </div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive, watch } from "vue";

const basePath = import.meta.env.VITE_APP_BASE_PATH;
let filter = reactive({
  type: "用户昵称",
  keyword: "嘟嘟嘟",
  page: 1,
  size: 10,
});
let loading = reactive({
  show: true,
  message: "正在加载元数据",
});
let error = reactive({
  show: false,
  message: "可恶，居然什么都没搜到",
});
let displayList = ref([]);
let summaryData = [];
let filteredList = [];
let filteredTotal = ref(1);
let announcement = ref("");

watch(
  () => filter.page,
  () => {
    search();
  }
);

watch(filter, () => {
  search();
});

fetch(`${basePath}/other-file/announcement`)
  .then((response) => response.text())
  .then((data) => {
    announcement.value = data;
  })
  .catch((err) => {
    console.log(err);
  });

const readomData = () => {
  for (let i = summaryData.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [summaryData[i], summaryData[j]] = [summaryData[j], summaryData[i]];
  }
  search();
};

const getSummaryData = () => {
  loading.message = "加载元数据中";
  loading.show = true;
  fetch(`${basePath}/summary.json`)
    .then((response) => response.json())
    .then((data) => {
      loading.show = false;
      summaryData = data;
      search();
    })
    .catch((err) => {
      loading.show = false;
      error.show = true;
      error.message = "加载元数据失败";
    });
};
getSummaryData();

const search = () => {
  filteredList = [];
  summaryData.forEach((item) => {
    if (filter.type == "帖子主题") {
      if (item.post_data.title.indexOf(filter.keyword) != -1) {
        filteredList.push({
          post_id: item.post_id,
          title: item.post_data.title,
          content: item.post_data.content[0].content,
          floor_num: 1,
          nickname: item.post_data.content[0].nickname,
          created_at: item.post_data.content[0].created_at,
        });
      }
    }
    if (filter.type == "用户昵称") {
      item.post_data.content.forEach((item1) => {
        if (item1.nickname.indexOf(filter.keyword) != -1) {
          filteredList.push({
            post_id: item.post_id,
            title: item.post_data.title,
            content: item1.content,
            floor_num: item1.floor_num,
            nickname: item1.nickname,
            created_at: item1.created_at,
          });
        }
      });
    }
    if (filter.type == "帖子内容") {
      item.post_data.content.forEach((item1) => {
        if (item1.content.indexOf(filter.keyword) != -1) {
          filteredList.push({
            post_id: item.post_id,
            title: item.post_data.title,
            content: item1.content,
            floor_num: item1.floor_num,
            nickname: item1.nickname,
            created_at: item1.created_at,
          });
        }
      });
    }
  });
  filteredTotal.value = filteredList.length;

  let c = filter.page * filter.size;
  let b = (filter.page - 1) * filter.size;
  if (c >= filteredList.length) {
    c = filteredList.length;
  }
  displayList.value = filteredList.slice(b, c);
  if (displayList.value.length == 0) {
    if (filter.page == 1) {
      error.show = true;
      error.message = "可恶，居然什么都没搜到";
    } else {
      filter.page = 1;
    }
  } else {
    error.show = false;
  }
};
</script>
