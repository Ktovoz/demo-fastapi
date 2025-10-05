<template>
  <CardContainer title="编辑角色" bordered>
    <Loading v-if="loading" overlay tip="正在加载角色信息" />
    <template v-else>
      <a-form layout="vertical" @finish="handleSubmit" :model="form">
        <a-form-item label="角色名称" name="displayName" :rules="[{ required: true, message: '请输入角色名称' }]"><a-input v-model:value="form.displayName" /></a-form-item>
        <a-form-item label="描述" name="description"><a-textarea v-model:value="form.description" rows="3" /></a-form-item>
        <a-form-item label="权限">
          <PermissionTree :tree-data="treeData" v-model:checkedKeys="form.permissions" />
        </a-form-item>
        <a-form-item label="状态">
          <a-radio-group v-model:value="form.status">
            <a-radio value="active">活跃</a-radio>
            <a-radio value="pending">待审核</a-radio>
            <a-radio value="inactive">禁用</a-radio>
          </a-radio-group>
        </a-form-item>
        <a-space>
          <a-button @click="goBack">取消</a-button>
          <a-button type="primary" html-type="submit" :loading="saving">保存</a-button>
        </a-space>
      </a-form>
    </template>
  </CardContainer>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import CardContainer from '../../components/layout/CardContainer.vue'
import PermissionTree from '../../components/business/PermissionTree.vue'
import Loading from '../../components/common/Loading.vue'
import { useRoleStore } from '../../store/role'

const route = useRoute()
const router = useRouter()
const roleStore = useRoleStore()

const loading = ref(true)
const saving = ref(false)

const form = reactive({
  displayName: '',
  description: '',
  permissions: [],
  status: 'active'
})

const treeData = [
  {
    title: '用户管理',
    key: 'users',
    children: [
      { title: '查看用户', key: 'users:view' },
      { title: '编辑用户', key: 'users:edit' },
      { title: '删除用户', key: 'users:delete' }
    ]
  },
  {
    title: '角色管理',
    key: 'roles',
    children: [
      { title: '查看角色', key: 'roles:view' },
      { title: '编辑角色', key: 'roles:edit' }
    ]
  },
  {
    title: '系统管理',
    key: 'system',
    children: [
      { title: '查看日志', key: 'logs:view' },
      { title: '管理系统', key: 'system:manage' }
    ]
  }
]

const loadRole = async () => {
  try {
    const role = await roleStore.fetchRoleDetail(route.params.id)
    Object.assign(form, {
      displayName: role.displayName,
      description: role.description,
      permissions: role.permissions ?? [],
      status: role.status ?? 'active'
    })
  } catch (error) {
    message.error('无法加载角色信息')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  saving.value = true
  try {
    await roleStore.updateRole(route.params.id, {
      displayName: form.displayName,
      description: form.description,
      permissions: [...form.permissions],
      status: form.status
    })
    message.success('角色更新成功')
    router.push('/roles/list')
  } catch (error) {
    message.error('保存角色失败')
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.push('/roles/list')
}

onMounted(loadRole)
</script>

