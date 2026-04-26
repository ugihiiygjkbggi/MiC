# 語法
* IEnumerable<T>//Interface
    ``` csharp
    IEnumerable<int> a = new List<int> {1, 2};
    IEnumerable<int> b = new int[] {1, 2};
    IEnumerable<int> c = Enumerable.Range(1, 5);//Range是一個方法，產生 1, 2, 3, 4, 5
    IEnumerable<int> e = [1, 2, 3];
    ```

* Array
    * 宣告
    ``` csharp
    int[] name = new int[5];
    int[] name = new int[] {1, 2, 3};
    int[] name = {1, 2, 3}; //宣告時才可以這樣用
    int[] name = [1, 2, 3]; //集合運算式
    ```
    * 常見方法
    ``` csharp
    var val = arr[0];//取值
    arr[0] = "New";//改值
    arr.Length;
    Array.Sort(arr);
    ```

* List<T>
  * 宣告
   ``` csharp
    List<Type> name = new List<Type>()
    List<Type> name = new List<Type>(){1,2,3}
    List<Type> name = new List<Type>{1,2,3}
    List<Type> name = new ()
    List<Type> name = new (){1,2,3}
    List<Type> name = [1,2,3]
    ```
  * 常見方法
  ``` csharp
  list.Count
  list.ForEach(x => Console.WriteLine(x));//List特有，非LINQ
  list.Add("John")
  list.AddRange("John","Marry")//或者myList.AddRange(newList);
  myList.Remove("魚");
  myList.RemoveRange("魚","貓");
  var found = list.Find(x => x > 10);

  ```
   
* Dictionary
  * 宣告
  ```csharp
  Dictionary<string, int> dict1 = new Dictionary<string, int>();
  Dictionary<string, int> dict2 = new Dictionary<string, int> {   { "Max", 100 }, { "Tom", 90 } };//初始化
  Dictionary<string, int> dict2 = new Dictionary<string, int> {   ["Max"] = 100,    ["Tom"] = 90 };
  Dictionary<string, int> dict4 = new() {     ["Max"] = 100 };
  ```
  * 常見方法 
  ``` csharp
  dict.Count//計算長度
  dict["Tom"] = 90;//改值
  if (dict.TryGetValue("Max", out var score)) { ... }//較安全的取值
  dict.Add("Max",5)
  dict.Remove("Max");
  dict.ContainsKey("Max")
  dict.ContainsValue("Max")
  Dictionary<int, string>.KeyCollection keys = dict.Keys;//取得所有Key，通常存起來再用Foreach跑
  Dictionary<int, string>.ValueCollection values = dict.Values;//取得所有Values
  ```
 

* LINQ
  >只要繼承IEnumerable，都可以用LINQ

* String
    ` string Name = "Anting";`
* Delegate
    ``` csharp
    Func<T1,T2,...,T> name = ()=>{}//後面是lambda expression
    ```
