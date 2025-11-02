export const navigationTree = [
  {
    key: 'users',
    label: '用户管理',
    icon: 'TeamOutlined',
    path: '/users/list',
    permission: 'users:view'
  },
  {
    key: 'roles',
    label: '角色管理',
    icon: 'SafetyOutlined',
    path: '/roles/list',
    permission: 'roles:view'
  },
  {
    key: 'profile',
    label: '个人资料',
    icon: 'ProfileOutlined',
    path: '/profile',
    permission: 'users:view'
  }
]

const buildIndex = (items, ancestors = [], acc = new Map()) => {
  for (const item of items) {
    acc.set(item.key, { item, parents: [...ancestors] })
    if (item.children?.length) {
      buildIndex(item.children, [...ancestors, item.key], acc)
    }
  }
  return acc
}

export const navigationIndex = buildIndex(navigationTree)

export const flattenNavigation = () => Array.from(navigationIndex.values()).map((entry) => entry.item)

export const findNavigationNode = (predicate, items = navigationTree, ancestors = []) => {
  for (const item of items) {
    if (predicate(item)) {
      return { item, parents: ancestors }
    }
    if (item.children?.length) {
      const child = findNavigationNode(predicate, item.children, [...ancestors, item.key])
      if (child) {
        return child
      }
    }
  }
  return null
}

export const findNavigationByPath = (path) =>
  findNavigationNode((item) => Boolean(item.path) && path.startsWith(item.path))
