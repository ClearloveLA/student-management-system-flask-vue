<template>
  <div class="student-container">
    <div class="toolbar">
      <el-button type="primary" @click="handleAdd">添加学生</el-button>
      <el-button type="success" @click="handleGenerateMock" :loading="generating">
        生成模拟数据
      </el-button>
    </div>

    <el-table v-loading="loading" :data="students">
      <el-table-column prop="id" label="学号" width="120" />
      <el-table-column prop="name" label="姓名" width="120" />
      <el-table-column prop="gender" label="性别" width="80" />
      <el-table-column prop="age" label="年龄" width="80" />
      <el-table-column prop="class_name" label="班级" />
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="enrollment_date" label="入学日期" width="120" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
          <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 编辑/添加对话框 -->
    <el-dialog
      :title="dialogType === 'add' ? '添加学生' : '编辑学生'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="学号" prop="id">
          <el-input v-model="form.id" :disabled="dialogType === 'edit'" />
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="form.gender">
            <el-option label="男" value="男" />
            <el-option label="女" value="女" />
          </el-select>
        </el-form-item>
        <!-- 其他表单项... -->
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getStudents, addStudent, updateStudent, deleteStudent } from '@/api/student'
import { generateMockData } from '@/api/system'

const loading = ref(false)
const generating = ref(false)
const students = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 获取学生列表
const fetchStudents = async () => {
  try {
    loading.value = true
    const res = await getStudents({
      page: currentPage.value,
      per_page: pageSize.value
    })
    students.value = res.items
    total.value = res.total
  } catch (error) {
    console.error('获取学生列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 生成模拟数据
const handleGenerateMock = async () => {
  try {
    generating.value = true
    await generateMockData()
    ElMessage.success('生成模拟数据成功')
    fetchStudents()
  } catch (error) {
    console.error('生成模拟数据失败:', error)
  } finally {
    generating.value = false
  }
}

// 删除学生
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该学生吗？')
    await deleteStudent(row.id)
    ElMessage.success('删除成功')
    fetchStudents()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
.student-container {
  padding: 20px;
}
.toolbar {
  margin-bottom: 20px;
}
.pagination {
  margin-top: 20px;
  text-align: right;
}
</style> 