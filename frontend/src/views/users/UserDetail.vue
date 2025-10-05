<template>
  <CardContainer title="用户详情" bordered>
    <Loading v-if="loading" overlay tip="正在加载用户信息" />
    <template v-else>
      <a-row :gutter="16">
        <a-col :span="6">
          <UserAvatar :name="user?.name" :src="user?.avatar" :size="90" />
        </a-col>
        <a-col :span="18">
          <a-descriptions bordered :column="2">
            <a-descriptions-item label="姓名">{{ user?.name }}</a-descriptions-item>
            <a-descriptions-item label="邮箱">{{ user?.email }}</a-descriptions-item>
            <a-descriptions-item label="角色">{{ user?.roleName }}</a-descriptions-item>
            <a-descriptions-item label="状态">
              <StatusTag :status="user?.status" />
            </a-descriptions-item>
            <a-descriptions-item label="部门">{{ user?.department }}</a-descriptions-item>
            <a-descriptions-item label="电话">{{ user?.phone || '未提供' }}</a-descriptions-item>
            <a-descriptions-item label="创建时间">{{ user?.createdAt }}</a-descriptions-item>
            <a-descriptions-item label="最后登录">{{ user?.lastLogin || '从未登录' }}</a-descriptions-item>
          </a-descriptions>
        </a-col>
      </a-row>
      <a-divider />
      <a-row :gutter="16">
        <a-col :span="12">
          <h3>标签</h3>
          <a-space wrap>
            <a-tag v-if="!user?.tags?.length">无标签</a-tag>
            <a-tag v-for="tag in user?.tags" :key="tag">{{ tag }}</a-tag>
          </a-space>
        </a-col>
        <a-col :span="12">
          <h3>权限</h3>
          <a-space wrap>
            <a-tag v-for="permission in user?.permissions" :key="permission">{{ permission }}</a-tag>
          </a-space>
        </a-col>
      </a-row>
      <a-divider />
      <a-space>
        <a-button @click="goBack">返回</a-button>
        <a-button type="primary" @click="editUser">编辑</a-button>
      </a-space>
    </template>
  </CardContainer>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import StatusTag from '../../components/business/StatusTag.vue'
import Loading from '../../components/common/Loading.vue'
import UserAvatar from '../../components/business/UserAvatar.vue'
import { useUserStore } from '../../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const user = ref(null)
const loading = ref(true)

const loadUser = async () => {
  try {
    user.value = await userStore.fetchUserDetail(route.params.id)
  } catch (error) {
    message.error('无法加载用户详情')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/users/list')
}

const editUser = () => {
  router.push(`/users/${route.params.id}/edit`)
}

onMounted(loadUser)
</script>

