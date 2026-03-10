# 在线问卷调查系统 API 接口文档

## 1. 认证相关接口

### 1.1 登录
- **请求方法**：POST
- **URL**：`/api/auth/login/`
- **参数**：
  - email: string (必填) - 邮箱
  - password: string (必填) - 密码
- **返回值示例**：
  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "status": 1,
      "created_at": "2026-03-10T15:00:00Z",
      "last_login": "2026-03-10T15:30:00Z"
    }
  }
  ```

### 1.2 注册
- **请求方法**：POST
- **URL**：`/api/users/users/`
- **参数**：
  - username: string (必填) - 用户名
  - email: string (必填) - 邮箱
  - password: string (必填) - 密码
  - role: string (可选) - 角色，默认'respondent'
- **返回值示例**：
  ```json
  {
    "id": 2,
    "username": "creator",
    "email": "creator@example.com",
    "role": "creator",
    "status": 1,
    "created_at": "2026-03-10T15:00:00Z",
    "last_login": null
  }
  ```

## 2. 用户相关接口

### 2.1 获取用户列表
- **请求方法**：GET
- **URL**：`/api/users/users/`
- **权限**：管理员
- **返回值示例**：
  ```json
  [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "status": 1,
      "created_at": "2026-03-10T15:00:00Z",
      "last_login": "2026-03-10T15:30:00Z"
    },
    {
      "id": 2,
      "username": "creator",
      "email": "creator@example.com",
      "role": "creator",
      "status": 1,
      "created_at": "2026-03-10T15:00:00Z",
      "last_login": null
    }
  ]
  ```

### 2.2 获取用户详情
- **请求方法**：GET
- **URL**：`/api/users/users/{id}/`
- **权限**：管理员或用户本人
- **返回值示例**：
  ```json
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "admin",
    "status": 1,
    "created_at": "2026-03-10T15:00:00Z",
    "last_login": "2026-03-10T15:30:00Z"
  }
  ```

## 3. 问卷模板相关接口

### 3.1 获取模板列表
- **请求方法**：GET
- **URL**：`/api/templates/`
- **返回值示例**：
  ```json
  [
    {
      "id": 1,
      "name": "市场调研模板",
      "description": "用于市场调研的通用模板",
      "content": {...},
      "category": "市场调研",
      "created_by": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      "created_at": "2026-03-10T15:00:00Z",
      "updated_at": "2026-03-10T15:00:00Z"
    }
  ]
  ```

### 3.2 创建模板
- **请求方法**：POST
- **URL**：`/api/templates/`
- **权限**：管理员
- **参数**：
  - name: string (必填) - 模板名称
  - description: string (可选) - 模板描述
  - content: object (必填) - 模板内容
  - category: string (可选) - 模板分类
- **返回值示例**：
  ```json
  {
    "id": 2,
    "name": "满意度调查模板",
    "description": "用于满意度调查的模板",
    "content": {...},
    "category": "满意度",
    "created_by": {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com"
    },
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

## 4. 问卷相关接口

### 4.1 获取问卷列表
- **请求方法**：GET
- **URL**：`/api/questionnaires/`
- **权限**：管理员（所有问卷）或创建者（自己的问卷）
- **返回值示例**：
  ```json
  [
    {
      "id": 1,
      "title": "产品满意度调查",
      "description": "请对我们的产品进行评价",
      "creator_id": {
        "id": 2,
        "username": "creator",
        "email": "creator@example.com"
      },
      "template_id": null,
      "status": "published",
      "start_time": "2026-03-10T00:00:00Z",
      "end_time": "2026-03-31T23:59:59Z",
      "max_responses": 1000,
      "ip_limit": 1,
      "allow_anonymous": 0,
      "is_public_result": 1,
      "questions": [...],
      "created_at": "2026-03-10T15:00:00Z",
      "updated_at": "2026-03-10T15:00:00Z"
    }
  ]
  ```

### 4.2 创建问卷
- **请求方法**：POST
- **URL**：`/api/questionnaires/`
- **权限**：管理员或创建者
- **参数**：
  - title: string (必填) - 问卷标题
  - description: string (可选) - 问卷描述
  - template_id: integer (可选) - 模板ID
  - status: string (必填) - 状态（draft, published, closed）
  - start_time: string (可选) - 开始时间
  - end_time: string (可选) - 结束时间
  - max_responses: integer (可选) - 最大填写次数
  - ip_limit: integer (可选) - 是否限制IP
  - allow_anonymous: integer (可选) - 是否允许匿名
  - is_public_result: integer (可选) - 是否公开结果
  - questions: array (可选) - 题目列表
- **返回值示例**：
  ```json
  {
    "id": 2,
    "title": "用户体验调查",
    "description": "请分享您的用户体验",
    "creator_id": {
      "id": 2,
      "username": "creator",
      "email": "creator@example.com"
    },
    "template_id": null,
    "status": "draft",
    "start_time": null,
    "end_time": null,
    "max_responses": 0,
    "ip_limit": 0,
    "allow_anonymous": 1,
    "is_public_result": 1,
    "questions": [...],
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

## 5. 题目相关接口

### 5.1 获取题目列表
- **请求方法**：GET
- **URL**：`/api/questions/`
- **权限**：管理员或创建者（自己问卷的题目）
- **返回值示例**：
  ```json
  [
    {
      "id": 1,
      "content": "您对我们的产品满意吗？",
      "type": "single",
      "options": ["非常满意", "满意", "一般", "不满意", "非常不满意"],
      "required": 1,
      "order": 0,
      "logic_rules": null,
      "created_at": "2026-03-10T15:00:00Z",
      "updated_at": "2026-03-10T15:00:00Z"
    }
  ]
  ```

### 5.2 创建题目
- **请求方法**：POST
- **URL**：`/api/questions/`
- **权限**：管理员或创建者
- **参数**：
  - questionnaire_id: integer (必填) - 问卷ID
  - content: string (必填) - 题目内容
  - type: string (必填) - 题目类型（single, multiple, text, scale）
  - options: array (可选) - 选项列表
  - required: integer (可选) - 是否必填
  - order: integer (可选) - 题目顺序
  - logic_rules: object (可选) - 跳转逻辑
- **返回值示例**：
  ```json
  {
    "id": 2,
    "content": "您使用我们的产品多久了？",
    "type": "single",
    "options": ["少于1个月", "1-3个月", "3-6个月", "6个月以上"],
    "required": 1,
    "order": 1,
    "logic_rules": null,
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

## 6. 填写相关接口

### 6.1 检查填写资格
- **请求方法**：GET
- **URL**：`/api/responses/check_eligibility/?questionnaire_id={id}`
- **返回值示例**：
  ```json
  {
    "eligible": true,
    "message": "You are eligible to fill this questionnaire"
  }
  ```

### 6.2 创建填写记录
- **请求方法**：POST
- **URL**：`/api/responses/`
- **参数**：
  - questionnaire_id: integer (必填) - 问卷ID
  - temp_data: object (可选) - 暂存数据
  - is_completed: integer (可选) - 是否完成
  - answers: array (可选) - 答案列表
- **返回值示例**：
  ```json
  {
    "id": 1,
    "questionnaire_id": {
      "id": 1,
      "title": "产品满意度调查"
    },
    "respondent_id": null,
    "ip_address": "127.0.0.1",
    "temp_data": {...},
    "is_completed": 0,
    "answers": [],
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

### 6.3 提交问卷
- **请求方法**：PUT
- **URL**：`/api/responses/{id}/`
- **参数**：
  - is_completed: integer (必填) - 设置为1表示完成
  - answers: array (必填) - 答案列表
- **返回值示例**：
  ```json
  {
    "id": 1,
    "questionnaire_id": {
      "id": 1,
      "title": "产品满意度调查"
    },
    "respondent_id": null,
    "ip_address": "127.0.0.1",
    "temp_data": null,
    "is_completed": 1,
    "answers": [
      {
        "id": 1,
        "question_id": {
          "id": 1,
          "content": "您对我们的产品满意吗？"
        },
        "value": "非常满意",
        "created_at": "2026-03-10T15:00:00Z"
      }
    ],
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

## 7. 数据分析相关接口

### 7.1 创建分析任务
- **请求方法**：POST
- **URL**：`/api/analysis-tasks/`
- **权限**：管理员或分析师
- **参数**：
  - questionnaire_id: integer (必填) - 问卷ID
  - task_name: string (必填) - 任务名称
  - export_format: string (必填) - 导出格式（Excel, SPSS）
- **返回值示例**：
  ```json
  {
    "id": 1,
    "analyst_id": {
      "id": 3,
      "username": "analyst",
      "email": "analyst@example.com"
    },
    "questionnaire_id": {
      "id": 1,
      "title": "产品满意度调查"
    },
    "task_name": "满意度分析",
    "status": "pending",
    "export_format": "Excel",
    "result_url": null,
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

### 7.2 获取分析任务列表
- **请求方法**：GET
- **URL**：`/api/analysis-tasks/`
- **权限**：管理员、分析师或创建者（自己问卷的任务）
- **返回值示例**：
  ```json
  [
    {
      "id": 1,
      "analyst_id": {
        "id": 3,
        "username": "analyst",
        "email": "analyst@example.com"
      },
      "questionnaire_id": {
        "id": 1,
        "title": "产品满意度调查"
      },
      "task_name": "满意度分析",
      "status": "completed",
      "export_format": "Excel",
      "result_url": "/path/to/result.xlsx",
      "created_at": "2026-03-10T15:00:00Z",
      "updated_at": "2026-03-10T15:30:00Z"
    }
  ]
  ```

## 8. 违规记录相关接口

### 8.1 获取违规记录列表
- **请求方法**：GET
- **URL**：`/api/violations/`
- **权限**：管理员
- **返回值示例**：
  ```json
  [
    {
      "id": 1,
      "questionnaire_id": {
        "id": 1,
        "title": "产品满意度调查"
      },
      "respondent_id": null,
      "ip_address": "127.0.0.1",
      "violation_type": "恶意填写",
      "description": "同一IP多次填写",
      "status": "pending",
      "processed_by": null,
      "processed_at": null,
      "created_at": "2026-03-10T15:00:00Z",
      "updated_at": "2026-03-10T15:00:00Z"
    }
  ]
  ```

### 8.2 创建违规记录
- **请求方法**：POST
- **URL**：`/api/violations/`
- **权限**：管理员
- **参数**：
  - questionnaire_id: integer (必填) - 问卷ID
  - respondent_id: integer (可选) - 填写者ID
  - ip_address: string (可选) - IP地址
  - violation_type: string (必填) - 违规类型
  - description: string (可选) - 描述
- **返回值示例**：
  ```json
  {
    "id": 2,
    "questionnaire_id": {
      "id": 1,
      "title": "产品满意度调查"
    },
    "respondent_id": null,
    "ip_address": "127.0.0.1",
    "violation_type": "恶意填写",
    "description": "同一IP多次填写",
    "status": "pending",
    "processed_by": null,
    "processed_at": null,
    "created_at": "2026-03-10T15:00:00Z",
    "updated_at": "2026-03-10T15:00:00Z"
  }
  ```

## 9. 权限说明

| 角色 | 权限 |
|------|------|
| 管理员 | 对所有表有CRUD权限，可管理用户、模板、系统设置，查看所有违规记录 |
| 问卷创建者 | 只能对自己的问卷进行增删改查，可引用公共模板创建问卷，可查看自己问卷的填写数据 |
| 填写者 | 只能填写已发布且未过期的问卷，若问卷设置了IP限制，同一IP只能填写一次 |
| 数据分析员 | 可查看所有问卷的原始数据，可创建分析任务，导出数据（Excel/SPSS），不能修改问卷内容 |

## 10. 问卷生命周期

- **草稿**：创建者编辑中，不可被填写
- **发布中**：在start_time到end_time之间，填写者可访问
- **已关闭**：超过结束时间或被创建者手动关闭，不可再填写

## 11. 跳转逻辑

在question表的logic_rules字段中，用JSON存储条件与目标题目ID，例如：

```json
{
  "conditions": [
    { "question_id": 5, "option_id": 2, "operator": "eq" }
  ],
  "target_question_id": 10,
  "action": "jump"
}
```

填写时，系统根据规则动态控制题目显示顺序。

## 12. 暂存功能

填写者在填写过程中可手动暂存，系统将当前答案保存到response.temp_data字段（JSON格式）。下次继续填写时，从temp_data加载已填内容。

## 13. 数据导出格式

- **Excel**：包含表头（题目）和每一行答案（每个答案一行，多选可合并为逗号分隔）
- **SPSS**：生成sav文件，需包含变量标签和值标签
