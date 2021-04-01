<?php

use JsonRPC\Client;
use JsonRPC\HttpClient;

class steemd
{

  protected $host;
  protected $client;

  public function __construct($host)
  {
    $this->host = $host;
    $httpClient = new HttpClient($host);
    $httpClient->withoutSslVerification();
    $this->client = new Client($host, false, $httpClient);
  }

  public function getState($path = "")
  {
    try {
      return $this->client->call(0, 'get_state', [$path]);
    } catch (Exception $e) {
      return array();
    }
  }

  public function getBlock($height)
  {
    try {
      return $this->client->call(0, 'get_block', [$height]);
    } catch (Exception $e) {
      return array();
    }
  }

  public function getAccount($account)
  {
    try {
      $return = $this->client->call(0, 'get_accounts', [[$account], false]);
      try {
        return $return[0][1];
      } catch (Exception $e) {
        var_dump($e); exit;
      }
    } catch (Exception $e) {
      var_dump($e); exit;
      return array();
    }
  }
  public function getAccountHistory($username, $limit = 100, $skip = -1)
  {
    try {
      return $this->client->call(0, 'get_account_history', [$username, -1, $limit]);
    } catch (Exception $e) {
      return array();
    }
  }

  public function getProps()
  {
    try {
      $return = $this->client->call(0, 'get_dynamic_global_properties', []);
      $return['muse_per_mvests'] = floor($return['total_vesting_fund_muse'] / $return['total_vesting_shares'] * 1000000 * 1000) / 1000;
      return $return;
    } catch (Exception $e) {
      return array();
    }
  }

  public function getChainProps()
  {
    try {
      $return = $this->client->call(0, 'get_chain_properties', []);
      return $return;
    } catch (Exception $e) {
      return array();
    }
  }

  public function getApi($name)
  {
    return $this->client->call(1, 'get_api_by_name', [$name]);
  }

  public function getFollowing($username, $limit = 100, $skip = -1)
  {
    $api = $this->getApi('follow_api');
    return $this->client->call($api, 'get_following', [$username, $skip, $limit]);
  }
}
