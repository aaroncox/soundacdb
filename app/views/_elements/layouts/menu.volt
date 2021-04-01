<div class="ui fixed inverted black main menu">
  <div class="ui container">
    <a class="launch icon item">
      <i class="content icon"></i>
    </a>

    <div class="right menu">
      <div class="ui category search item">
        <div class="ui icon input">
          <input class="prompt" type="text" placeholder="Search accounts...">
          <i class="search icon"></i>
        </div>
        <div class="results"></div>
      </div>
    </div>
  </div>
</div>
<!-- Following Menu -->
<div class="ui black inverted top fixed mobile hidden menu">
  <div class="ui container">
    <a href="/" class="header {{ (router.getControllerName() == 'index') ? 'active' : '' }} item">
      <div class="ui floating labeled">
        <img style="border-radius: 0; height: 24px" src="/logo.png"/>
      </div>
    </a>
    <a href="/accounts" class="{{ (router.getControllerName() == 'account' or router.getControllerName() == 'accounts') ? 'active' : '' }} item">Accounts</a>
    <a href="/witnesses" class="{{ (router.getControllerName() == 'witness') ? 'active' : '' }} item">Block Producers</a>
    <div class="right menu">
      <div class="ui category search item">
        <div class="ui icon input">
          <input class="prompt" type="text" placeholder="Search accounts...">
          <i class="search icon"></i>
        </div>
        <div class="results"></div>
      </div>
    </div>
  </div>
</div>

<!-- Sidebar Menu -->
<div class="ui vertical inverted sidebar menu">
  <a href="/" class="{{ (router.getControllerName() == 'index') ? 'active' : '' }} item">home</a>
  <a href="/accounts" class="{{ (router.getControllerName() == 'account' or router.getControllerName() == 'accounts') ? 'active' : '' }} item">Accounts</a>
  <a href="/witnesses" class="{{ (router.getControllerName() == 'witness') ? 'active' : '' }} item">Block Producers</a>
</div>
