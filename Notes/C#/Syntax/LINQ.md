# LINQ


## 篩選用
* Where
  `list.Where(x => x.Age > 18)`
* Distinct
  >去除重複資料
  `list.Distinct()`
* OfType<T>
  >找出特定型別
  `list.OfType<Dog>()`

## Select
* Select
  >只拿取物件的某個屬性，或轉換成新物件
  `list.Select(x => x.Name)`
* SelectMany
  >把「清單中的清單」攤平成一個大清單
  `list.SelectMany(x => x.Orders)`

## Ordering
* OrderBy
  >由小到大排序
  `list.OrderBy(x => x.Price)`
* OrderByDescending
  >由大到小排序
  `list.OrderByDescending(x => x.Price)`
* ThenBy
  >次要排序
  `.OrderBy(x => x.Age).ThenBy(x => x.Name)`
* Reverse
  >次序反轉
  `list.Reverse()`

## 計算
* Count 
  `list.Count(x => x.Age > 20)`
* Sum
  `list.Sum(x => x.Price)`
* Average
  `list.Average(x => x.Score)`
* Max/Min
  `list.Max(x => x.Height)`

## Join
* Method Syntax
```csharp
var result = 外層集合.Join(
    內層集合,                      // 1. 想跟誰連？
    outer => outer.Key,          // 2. 我的關聯欄位
    inner => inner.Key,          // 3. 他的關聯欄位
    (outer, inner) => new { ... } // 4. 湊在一起後的樣子
);
```
* Query Syntax
```csharp
var result = from outer in 外層集合
             join inner in 內層集合 on outer.Key equals inner.Key
             select new { ... };
```

## others
* FirstOrDefault
  >抓第一個。找不到回傳 null
  `list.FirstOrDefault(x => x.Id == 1)`
* LastOrDefault
  >抓最後一個
  `list.LastOrDefault()`
* Any
  >是否有任何一個符合？
  `list.Any(x => x.IsActive`
* All
  >是否全部都符合？
 `list.All(x => x.Price > 0)`
* Contains
  >檢查集合中是否包含某個特定物件
  `list.Contains(item)`
* Take
  >拿前面幾筆資料
  `list.Take(10)`
* TakeWhile
  >拿前面幾筆資料直到遇到不符合條件
  `list.TakeWhile(x => x < 100)`
* Skip
  >跳過前幾筆資料
  `list.Skip(10)`
*  ToList
  >將結果存入 List<T> (會立刻執行)。
  `query.ToList()`
* ToArray
  >將結果存入陣列
  `query.ToArray()`

### Anonymous Types
    >常搭配LINQ使用
    ```csharp
    Select(p => new { p.FirstName, p.LastName })//當只想提取Class的一部分欄位
    Select(p => new { p.Name, Score = Random.Shared.Next(100) })//新增欄位
    GroupBy(p => new { p.City, p.Gender })//分組時，Composite key用
    ```