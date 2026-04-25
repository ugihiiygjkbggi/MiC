# 語法

* Array
    ``` csharp
    int[] name = new int[5];
    int[] name = new int[] {1, 2, 3};
    int[] name = [1, 2, 3]; //集合運算式
    ```
* List
    ``` csharp
    List<Type> name = new List<Type>()
    
* String
    ` string Name = "Anting";`
* Delegate
    ``` csharp
    Func<T1,T2,...,T> name = ()=>{}//後面是lambda expression
    ```
* Anonymous Types
    >常搭配LINQ使用
    ```csharp
    Select(p => new { p.FirstName, p.LastName })//當只想提取Class的一部分欄位
    Select(p => new { p.Name, Score = Random.Shared.Next(100) })//新增欄位
    GroupBy(p => new { p.City, p.Gender })//分組時，Composite key用
    ```