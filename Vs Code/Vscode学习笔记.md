## Vscode 全局搜索无法搜索到某一个文件夹

![配置设置](./picture/SearchSetting.png)

## Vscode 配置搜索文件及非搜索文件

在**settings.json**内添加需要排除的文件,如排除build目录

```json
"files.exclude": {
        "**/build": true
    },
```

