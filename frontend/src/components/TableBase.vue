<template>
  <div class="table-responsive">
    <table class="table table-hover">
      <thead class="table-light">
        <tr>
          <th 
            v-for="column in columns" 
            :key="column.key"
            scope="col"
            :class="{ 'sortable': column.sortable }"
            @click="column.sortable && handleSort(column.key)"
          >
            {{ column.label }}
            <i 
              v-if="column.sortable && sortKey === column.key"
              :class="['fas', sortOrder === 'asc' ? 'fa-sort-up' : 'fa-sort-down']"
            ></i>
          </th>
          <th v-if="$slots.actions" scope="col" class="text-end">Akcje</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in sortedData" :key="item.id || item.key">
          <td v-for="column in columns" :key="column.key">
            <slot :name="`cell-${column.key}`" :item="item" :value="item[column.key]">
              {{ formatValue(item[column.key], column.type) }}
            </slot>
          </td>
          <td v-if="$slots.actions" class="text-end">
            <slot name="actions" :item="item"></slot>
          </td>
        </tr>
      </tbody>
    </table>
    
    <div v-if="!data.length" class="text-center py-4 text-muted">
      <slot name="empty">
        Brak danych do wyświetlenia
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Column {
  key: string
  label: string
  sortable?: boolean
  type?: 'text' | 'date' | 'number' | 'currency'
}

interface Props {
  data: any[]
  columns: Column[]
}

const props = defineProps<Props>()

const sortKey = ref<string>('')
const sortOrder = ref<'asc' | 'desc'>('asc')

const sortedData = computed(() => {
  if (!sortKey.value) return props.data
  
  return [...props.data].sort((a, b) => {
    const aVal = a[sortKey.value]
    const bVal = b[sortKey.value]
    
    if (aVal < bVal) return sortOrder.value === 'asc' ? -1 : 1
    if (aVal > bVal) return sortOrder.value === 'asc' ? 1 : -1
    return 0
  })
})

const handleSort = (key: string) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
}

const formatValue = (value: any, type?: string) => {
  if (value === null || value === undefined) return '-'
  
  switch (type) {
    case 'date':
      return new Date(value).toLocaleDateString('pl-PL')
    case 'currency':
      return `${value} PLN`
    case 'number':
      return value.toLocaleString('pl-PL')
    default:
      return value
  }
}
</script>

<style scoped>
.sortable {
  cursor: pointer;
  user-select: none;
}

.sortable:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.table-responsive {
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>