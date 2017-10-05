# フォント

http://wikinavi.net/vipgamecreator/index.php?%E3%82%B2%E3%83%BC%E3%83%A0%E3%81%AB%E4%BD%BF%E3%81%88%E3%82%8B%E3%83%95%E3%82%A9%E3%83%B3%E3%83%88

任意のフォントファイルを配布し、それを参照して文字を表示する。

もしフォントファイルを配布しないと表示されない可能性がある。


循環インポート発生。実装方法を考えねばならない。



# 現状の概要

* Mainクラスはpygameの骨組み（メインループ）
* StateSwitcherクラスはゲーム状態の管理と制御
* GameState系クラスはpygameのイベント処理と分岐
* GameCommandクラスはゲーム処理の実装

## 案

```python
SelectState.Initialize = GameCommand.NewGhostleg
SelectState.Finalize = クラス内実装
SelectState.Event = クラス内実装
SelectState.Draw = クラス内実装

AnimateState.Initialize = GameCommand.StartAnimation
AnimateState.Finalize = GameCommand.EndAnimation
AnimateState.Draw = GameCommand.Animation
AnimateState.Event = クラス内実装

ResultState.Initialize = GameCommand.StartGoalPerformance
ResultState.Finalize = GameCommand.EndGoalPerformance
ResultState.Event = クラス内実装
ResultState.Draw = GameCommand.GoalPerformance
```




# どうしよう

* Main
* GameStateManager
    * StateSwitcher
    * GameState
        * Select
        * Animate
        * Result
    * GameCommand

StateSwitcher、Main、各状態クラス、の関係を修正したほうがいい。「Main<--Switcher<-->各State」という関係が複雑。「Main<--Manager<--Switcher,Factory<--State」という関係にしたほうが簡単になるか。

## GameStateAssociator

各ゲーム状態を関連付ける。ゲーム状態の遷移パターン次第で関連付けの方法も変わる。

### 案1

* 順序付け（Next()）
* 直接指定（Select(StateClass)）

### 案2

各ゲーム状態のInitialize, Finalizeにゲームコマンドを対応付ける。

```python
SelectState.Initialize = GameCommand.NewGhostleg
SelectState.Finalize = クラス内実装
SelectState.Event = クラス内実装（ゲーム状態遷移）
SelectState.Draw = クラス内実装

AnimateState.Initialize = GameCommand.StartAnimation
AnimateState.Finalize = GameCommand.EndAnimation
AnimateState.Draw = GameCommand.Animation（ゲーム状態遷移）
AnimateState.Event = クラス内実装

ResultState.Initialize = GameCommand.StartGoalPerformance
ResultState.Finalize = GameCommand.EndGoalPerformance
ResultState.Event = クラス内実装（ゲーム状態遷移）
ResultState.Draw = GameCommand.GoalPerformance
```

各ゲーム状態固有の実装はそのモジュールやクラス内で実装する。

各ゲーム状態固有でなく、他の状態への遷移や、他のゲームデータを参照するメソッド定義はGameStateAssociatorで定義する。こうすることで、GameCommandインスタンスの参照を各状態クラスへ渡さなくても済む。

# ゲーム状態の遷移

* 「Select→Animate→Result」に固定してしまうと簡単になる。SwitcherはNext()だけになる。呼出元もNext()に固定できる。
* 「Select←→Animate←→Result」や、直接指定できるようにしてもいいが、今回は必要性がない。わずかにキー操作が減らせる程度の恩恵しかない

## 各ゲーム状態の共通操作

* ゲーム状態の遷移
* ゲームコマンドの実行

これ以外は各ゲーム状態固有の実装をする。

共通操作をどのように実装するかがポイント。単にインスタンスの参照を各クラスに渡したら以下のような問題が生じる。

* 参照渡しの引数がうざい
    * 変更されたとき修正が必要
* インスタンスの全メソッドが呼べてしまう

## ゲーム状態遷移とそのメソッド

各ゲーム状態クラスは、必ずゲーム状態遷移を行う。

* どのようなときに
* 何の状態遷移メソッドを実行するのか

各ゲーム状態クラスごとに異なる。

### どのようなときに

各状態クラス内で実装すべき。各状態クラス内固有の状態によって判断すべきときがあるかもしれないから。

### 何の状態遷移メソッドを実行するのか

GameStateAssociatorで決めたほうがいい。個々の状態に設定するのではなく、全体の関係を設定するクラスで実装すべき。見渡せるから。

* 予め状態遷移の全パターンを決めておく（Next, Prev, First, Last, Select）
* 各状態クラスごとに必要なパターンの条件を内部で実装させる
    * pygameのevent, screenインスタンスも必要かもしれない

```python
SelectState.IsNext = lambda: return event.key == K_RETURN
AnimateState.IsNext = lambda: return AnimateState.IsFinished() # 状態クラス内部で定義すべき（状態クラス内部変数を参照して判定するから）
```


```python
GameState.Event(event):
    GameState.__SwitchState(event)
    ...任意...

GameState.__SwitchState(event):
    if self.IsNext(event): self.Switcher.Next()
    if self.IsPrev(event): self.Switcher.Prev()
    if self.IsFirst(event): self.Switcher.First()
    if self.IsLast(event): self.Switcher.Last()
    s = self.IsSelect(event)
    if s: self.Switcher.Select(s)
```

```python
class StateSwitchCondition:
    def IsNext(self): return False
    def IsPrev(self): return False
    def IsFirst(self): return False
    def IsLast(self): return False
    def SelectState(self): return None
```
```python
class GameState:
    def __new__(...):
        attrs['__stateSwitchCondition'] = StateSwitchCondition()
class SelectState(GameState):
    def __init__(self):
        self.__stateSwitchCondition.IsNext = self.__IsNext
    def IsNext(self):
        if self.__event.key == K_RETURN or self.__event.key == K_SPACE or self.__event.key == K_z: 
            #self.__stateSwitcher.Next()
            return True
        else: return False
#    @GameState._GameState__SwitchState
    def Event(self):
        super()._GameState__SwitchState()
        ...任意の処理...
```


* どんな処理を、何のクラスで実装すべきか
* 各状態クラスが参照すべき他クラスは何か
    * event
    * screen
    * Switcher
    * GameCommand
        * Ghostleg
        * ...
* 全状態クラスが絶対行うことは何か
    * Event
        * ゲーム状態遷移
    * Draw
    * Initialize
    * Finalize
* ゲームコマンドと各状態における実行契機の関係
    * SelectState.Initialize = GameCommand.NewGhostleg
    * ...

ゲーム状態遷移の実装を体系化したい。

* 呼出部分はメインループで呼び出したい（各ゲーム状態クラスでは呼び出したくない（呼び忘れしうるから））

```python
def Run(self):
    pygame.init()
    if self.__title: pygame.display.set_caption(self.__title)
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit();
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: pygame.quit(); sys.exit();
            self.__stateSwitcher.State.Switch(self.__stateSwitcher, event) # ゲーム状態遷移
            self.__stateSwitcher.State.Event(event)
        self.__stateSwitcher.State.Draw(self.__screen.Screen)
        pygame.display.flip()
        clock.tick(60) # 60 FPS
```

上記のようにすれば、switcherクラスのインスタンスを各クラスのメンバに持たせずに済む。関係ないメソッドで実行されずに済む。

これと同様に、ゲームコマンドもMainから渡してしまえばいいかもしれない。

```python
def Run(self):
    pygame.init()
    if self.__title: pygame.display.set_caption(self.__title)
    clock = pygame.time.Clock()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit();
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: pygame.quit(); sys.exit();
            self.__stateSwitcher.State.SwitchState(self.__stateSwitcher, event) # ゲーム状態遷移
            self.__stateSwitcher.State.ProcessEvent(self.__gamecommand, event)
        self.__stateSwitcher.State.Draw(self.__screen.Screen)
        pygame.display.flip()
        clock.tick(60) # 60 FPS
```

* どのゲーム状態のとき、何を行うのか
    * どのゲーム状態のとき、どんなeventのとき、どのゲームコマンドを実行するのか
    * どのゲーム状態のとき、Nextすると、どの状態に遷移するのか





# ゲームのコマンド

ゲームのコマンドとは、ゲーム固有のコマンドのことである。コマンドの内容は処理である。呼出元ではゲームコマンドの実行に必要なクラスや引数などを隠蔽したい。

## コマンド一覧

コマンド|説明
--------|----
あみだくじ新規作成|初回、結果表示からの再開のときに新しいあみだくじを作成する。
アニメーション開始|あみだくじで線を選択後、アニメーションを開始する。
アニメーション完了|アニメーション最中でも強制的に完了した状態にする。（座標の頂点リストを瞬時に完成させる）
結果演出開始|あみだくじのアニメーション完了後、効果音など何らかの演出をする。
結果演出終了|たとえば効果音などが鳴っている最中なら消す。

## 実行タイミング

ゲーム状態が変更された時に実行したい。各Stateクラスに以下のメソッドを実装させ、Switcherクラスで呼び出す。

* Initialize()
* Finalize()

## 共通クラス

* Screen
* CalcSize
* Ghostleg
* LinesAnimation

上記のような、各ゲームコマンドで利用するクラスをどう隠蔽するか。次回の課題。


```python
class CommonClasses:
    def __init__(self):
        self.__screen = Screen
        ...
    @property
    def Screeen(self): return self.__screen
    ...
```
```python
class GameCommand:
    def __init__(self):
        self.__common = CommonClasses
    def NewGhostleg(self):
        pass
    def StartAnimation(self):
        pass
    def EndAnimation(self):
        pass
    def StartGoalPerformance(self):
        pass
    def EndGoalPerformance(self):
        pass
```




















# ゲームのコマンド

ゲームのコマンドとは、ゲーム固有のコマンドのことである。

## 実装方法

デザインパターンのうちコマンドパターンを使ってはどうか。

すでにゲームの状態はStateパターンにて実装した。次は「状態」よりも細かい「コマンド」について実装したい。

## コマンド一覧

コマンド|説明
--------|----
あみだくじ新規作成|初回、結果表示からの再開のときに新しいあみだくじを作成する。
アニメーション開始|あみだくじで線を選択後、アニメーションを開始する。
結果演出|あみだくじのアニメーション完了後、効果音など何らかの演出をする。


## pythonにおけるデザパタ参考

* http://oneshotlife-python.hatenablog.com/entry/2016/03/21/225915
    * https://github.com/faif/python-patterns

