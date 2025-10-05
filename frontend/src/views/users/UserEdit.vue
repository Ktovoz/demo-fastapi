<template>
  <CardContainer :title="pageTitle" bordered>
    <a-form layout="vertical" @finish="handleSubmit" :model="form" :disabled="loading">
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="姓名" name="name" :rules="[{ required: true, message: '请输入姓名' }]">
            <a-input v-model:value="form.name" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="邮箱" name="email" :rules="[{ required: true, message: '请输入邮箱' }]">
            <a-input v-model:value="form.email" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="角色" name="role">
            <a-select v-model:value="form.role" :options="roleOptions" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="状态" name="status">
            <a-select v-model:value="form.status" :options="statusOptions" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-row :gutter="16">
        <a-col :span="12">
          <a-form-item label="部门" name="department">
            <a-select v-model:value="form.department" :options="departmentOptions" />
          </a-form-item>
        </a-col>
        <a-col :span="12">
          <a-form-item label="电话" name="phone">
            <a-input v-model:value="form.phone" />
          </a-form-item>
        </a-col>
      </a-row>
      <a-form-item label="标签" name="tags">
        <a-select v-model:value="form.tags" mode="tags" placeholder="添加标签" />
      </a-form-item>
      <a-form-item label="权限" name="permissions">
        <a-select v-model:value="form.permissions" mode="multiple" :options="permissionOptions" />
      </a-form-item>
      <a-space>
        <a-button @click="goBack">取消</a-button>
        <a-button type="primary" html-type="submit" :loading="submitting">保存</a-button>
      </a-space>
    </a-form>
  </CardContainer>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import { useUserStore } from '../../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const submitting = ref(false)
const isCreate = computed(() => route.name === 'UserCreate')

const form = reactive({
  name: '',
  email: '',
  role: 'user',
  status: 'active',
  department: 'Operations',
  phone: '',
  tags: [],
  permissions: ['users:view']
})

const roleOptions = [
  { label: '管理员', value: 'admin' },
  { label: '经理', value: 'manager' },
  { label: '客服', value: 'support' },
  { label: '普通用户', value: 'user' }
]

const statusOptions = [
  { label: '活跃', value: 'active' },
  { label: '禁用', value: 'inactive' },
  { label: '待审核', value: 'pending' }
]

const departmentOptions = [
  { label: '运营部', value: 'Operations' },
  { label: '工程部', value: 'Engineering' },
  { label: '客服部', value: 'Support' },
  { label: '财务部', value: 'Finance' }
]

const permissionOptions = [
  { label: '查看用户', value: 'users:view' },
  { label: '编辑用户', value: 'users:edit' },
  { label: '删除用户', value: 'users:delete' },
  { label: '查看日志', value: 'logs:view' },
  { label: '管理系统', value: 'system:manage' }
]

const pageTitle = computed(() => (isCreate.value ? '创建用户' : '编辑用户'))

const loadUser = async () => {
  if (isCreate.value) {
    loading.value = false
    return
  }
  try {
    const user = await userStore.fetchUserDetail(route.params.id)
    Object.assign(form, {
      name: user.name,
      email: user.email,
      role: user.role,
      status: user.status,
      department: user.department,
      phone: user.phone,
      tags: user.tags ?? [],
      permissions: user.permissions ?? []
    })
  } catch (error) {
    message.error('无法加载用户信息')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const payload = {
      ...form,
      tags: [...(form.tags || [])],
      permissions: [...(form.permissions || [])]
    }
    if (isCreate.value) {
      await userStore.createUser(payload)
      message.success('用户创建成功')
    } else {
      await userStore.updateUser(route.params.id, payload)
      message.success('用户更新成功')
    }
    router.push('/users/list')
  } catch (error) {
    message.error('保存用户失败')
  } finally {
    submitting.value = false
  }
}

const goBack = () => {
  router.push('/users/list')
}

onMounted(loadUser)
</script>

