<template>
  <CardContainer title="User Detail" bordered>
    <Loading v-if="loading" overlay tip="Loading user" />
    <template v-else>
      <a-row :gutter="16">
        <a-col :span="6">
          <UserAvatar :name="user?.name" :src="user?.avatar" :size="90" />
        </a-col>
        <a-col :span="18">
          <a-descriptions bordered :column="2">
            <a-descriptions-item label="Name">{{ user?.name }}</a-descriptions-item>
            <a-descriptions-item label="Email">{{ user?.email }}</a-descriptions-item>
            <a-descriptions-item label="Role">{{ user?.roleName }}</a-descriptions-item>
            <a-descriptions-item label="Status">
              <StatusTag :status="user?.status" />
            </a-descriptions-item>
            <a-descriptions-item label="Department">{{ user?.department }}</a-descriptions-item>
            <a-descriptions-item label="Phone">{{ user?.phone || 'Not provided' }}</a-descriptions-item>
            <a-descriptions-item label="Created">{{ user?.createdAt }}</a-descriptions-item>
            <a-descriptions-item label="Last Login">{{ user?.lastLogin || 'Never' }}</a-descriptions-item>
          </a-descriptions>
        </a-col>
      </a-row>
      <a-divider />
      <a-row :gutter="16">
        <a-col :span="12">
          <h3>Tags</h3>
          <a-space wrap>
            <a-tag v-if="!user?.tags?.length">No tags</a-tag>
            <a-tag v-for="tag in user?.tags" :key="tag">{{ tag }}</a-tag>
          </a-space>
        </a-col>
        <a-col :span="12">
          <h3>Permissions</h3>
          <a-space wrap>
            <a-tag v-for="permission in user?.permissions" :key="permission">{{ permission }}</a-tag>
          </a-space>
        </a-col>
      </a-row>
      <a-divider />
      <a-space>
        <a-button @click="goBack">Back</a-button>
        <a-button type="primary" @click="editUser">Edit</a-button>
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
    message.error('Unable to load user detail')
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

