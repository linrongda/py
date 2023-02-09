---
title: 个人项目 v1.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.17"

---

# 个人项目

> v1.0.0

Base URLs:

# Default

## GET hello

GET /

> 返回示例

> 成功

```json
{
  "code": 200,
  "msg": "hello提示：id仅限integer整数，title、context、keyword均为string文本（title限255个字符，context限65535个字符，keyword长度限制未知），status仅可在“待办”和\"已完成\"中选择，addtime和deadline输入格式为：xxxx-xx-xx xx:xx:xx，all值根据需要填写，需要时填写任意True值均可。查询时，如果不通过id方法，则需要在路径后加上?page=数字&per_page=数字，更改其中“数字”为你需要的数字，page为第几页，per_page为每页显示多少条数据"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» msg|string|true|none||none|

## POST add

POST /todo

> Body 请求参数

```json
{
  "title": "a",
  "context": "b",
  "status": "待办",
  "addtime": "2023-2-9 01:01:01",
  "deadline": "2023-2-9 10:10:10"
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» title|body|string| 是 | 标题|限255个字符|
|» context|body|string| 是 | 内容|限65535个字符|
|» status|body|string| 是 | 完成状态|“待办”和“已完成”二选一|
|» addtime|body|string(date-time)| 是 | 添加时间|格式：xxxx-xx-xx xx:xx:xx|
|» deadline|body|string(date-time)| 是 | 截止时间|格式：xxxx-xx-xx xx:xx:xx|

#### 枚举值

|属性|值|
|---|---|
|» status|待办|
|» status|已完成|

> 返回示例

> 成功

```json
{
  "code": 200,
  "data": "title=a, context=b, status=待办, addtime=2023-2-9 00:00:00,deadline=2023-2-9 00:00:00",
  "msg": "添加成功"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

*失败返回code和msg，成功返回code、msg、data*

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|string|true|none||none|
|» msg|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|code|200|
|code|404|

## GET query

GET /todo

> Body 请求参数

```json
{
  "id": 1,
  "status": "待办",
  "all": "True",
  "keyword": "ab"
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|page|query|integer| 否 ||当前第几页页面|
|per_page|query|integer| 否 ||每页显示多少条数据|
|body|body|object| 否 ||none|
|» id|body|integer| 否 | id|none|
|» status|body|string| 否 | 完成状态|none|
|» all|body|boolean| 否 | 是否全部|none|
|» keyword|body|string| 否 | 关键字|none|

#### 枚举值

|属性|值|
|---|---|
|» status|待办|
|» status|已完成|

> 返回示例

> 成功

```json
{
  "code": 200,
  "data": "{'id': 45, 'title': 'a', 'context': 'b', 'status': '待办', 'addtime': datetime.datetime(2023, 2, 9, 1, 1, 1), 'deadline': datetime.datetime(2023, 2, 9, 10, 10, 10)}",
  "msg": "查询成功"
}
```

```json
{
  "code": 404,
  "msg": "查询失败，原因：该id不存在"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

*失败返回code和msg，成功返回code、msg、data*

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|string|true|none||none|
|» msg|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|code|200|
|code|404|

## PUT update

PUT /todo

> Body 请求参数

```json
"{\r\n    \"id\":1,\r\n    \"all\":\"True\"\r\n    \"status\":\"待办\"\r\n}"
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» id|body|integer| 否 | id|none|
|» all|body|boolean| 否 | 是否全部|none|
|» status|body|string| 是 | 完成状态|none|

#### 枚举值

|属性|值|
|---|---|
|» status|待办|
|» status|已完成|

> 返回示例

> 成功

```json
{
  "code": 200,
  "data": "成功将所有的待办事项修改为已完成状态",
  "msg": "更新成功"
}
```

```json
{
  "code": 200,
  "data": "成功将所有已完成的事项修改为待办状态",
  "msg": "更新成功"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

*失败返回code和msg，成功返回code、msg、data*

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|string|true|none||none|
|» msg|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|code|200|
|code|404|

## DELETE delete

DELETE /todo

> Body 请求参数

```json
{
  "id": 1,
  "all": "True",
  "status": "待办"
}
```

### 请求参数

|名称|位置|类型|必选|中文名|说明|
|---|---|---|---|---|---|
|body|body|object| 否 ||none|
|» id|body|integer| 否 | id|none|
|» all|body|boolean| 否 | 是否全部|none|
|» status|body|string| 否 | 完成状态|none|

#### 枚举值

|属性|值|
|---|---|
|» status|待办|
|» status|已完成|

> 返回示例

> 成功

```json
{
  "code": 200,
  "data": "成功将id=1的事项删除",
  "msg": "删除成功"
}
```

```json
{
  "code": 200,
  "data": "成功将所有的事项删除",
  "msg": "删除成功"
}
```

```json
{
  "code": 200,
  "data": "成功将所有已完成的事项删除",
  "msg": "删除成功"
}
```

```json
{
  "code": 200,
  "data": "成功将所有待办的事项删除",
  "msg": "删除成功"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|成功|Inline|

### 返回数据结构

状态码 **200**

*失败返回code和msg，成功返回code、msg、data*

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» code|integer|true|none||none|
|» data|string|true|none||none|
|» msg|string|true|none||none|

#### 枚举值

|属性|值|
|---|---|
|code|200|
|code|404|

# 数据模型

