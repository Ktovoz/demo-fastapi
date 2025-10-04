const resolvePath = (source, path) => {
  if (!path) return undefined
  return path.split('.').reduce((current, key) => {
    if (current == null) return undefined
    return current[key]
  }, source)
}

export const simulateResponse = (payload, options = {}) => {
  const { delay = 300, status = 200 } = options
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ status, data: payload })
    }, delay)
  })
}

export const paginateList = (items = [], pagination = {}) => {
  const { page = 1, pageSize = 10 } = pagination
  const start = (page - 1) * pageSize
  const end = start + pageSize
  return {
    items: items.slice(start, end),
    total: items.length,
    page,
    pageSize
  }
}

export const filterByKeyword = (items = [], keyword, fields = []) => {
  if (!keyword) return items
  const lowered = String(keyword).toLowerCase()
  return items.filter((item) =>
    fields.some((field) => {
      const value = resolvePath(item, field)
      return value != null && String(value).toLowerCase().includes(lowered)
    })
  )
}

export const sortByField = (items = [], sorter) => {
  if (!sorter?.field) return items
  const { field, order } = sorter
  const sorted = [...items].sort((a, b) => {
    const aValue = resolvePath(a, field)
    const bValue = resolvePath(b, field)
    if (aValue === bValue) return 0
    if (aValue == null) return -1
    if (bValue == null) return 1
    if (typeof aValue === "number" && typeof bValue === "number") {
      return aValue - bValue
    }
    return String(aValue).localeCompare(String(bValue))
  })
  return order === "descend" ? sorted.reverse() : sorted
}

export const withMeta = (items, meta = {}) => ({
  items,
  ...meta
})
