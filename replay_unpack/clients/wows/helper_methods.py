from .player import ReplayPlayer

class Helper:
  def __init__(self, player: ReplayPlayer):
      self.player = player


  # retrieve a sorted list of all timestamps associated with 
  # position data
  def get_sorted_times(self):
      times = []
      movements = self.player.get_movements()
      healths = self.player.get_health()
      for ent in movements:
        for pos in movements[ent]:
          times.append(pos[2])
      times = sorted(list(set(times)))
      return times

  #restructure position and health data to be a dict mapping each 
  # time stamp to a dict mapping shipId to position and health data 
  # for that time
  def get_data_by_time(self):
      player = self.player
      movements = player.get_movements()
      healths = player.get_health()
      data_by_time = {}
      
      ids = movements.keys()
      last_known_data = {}
      for id in ids: last_known_data[id] = None

      for entityId in movements:
        for ind, pos in enumerate(movements[entityId]):
          if pos[2] not in data_by_time: data_by_time[pos[2]] = {}
          data_by_time[pos[2]][entityId] = [pos[0], pos[1], healths[entityId][ind]]

      for time in data_by_time:
        no_data_keys = list(set(last_known_data.keys()) - set(data_by_time[time].keys()))
        for key in no_data_keys:
          if last_known_data[key] != None:data_by_time[time][key] = last_known_data[key]

        for val in data_by_time[time]:
          last_known_data[val] = data_by_time[time][val]

      return data_by_time

  # get team number for each ship
  def get_teams(self):
      player_info = self.player.get_info()['players']
      teams = {}
      for p in player_info: teams[player_info[p]['shipId']] = player_info[p]['teamId']
      return teams

  # get the username for each shipId
  def get_display_names(self):
      player_info = self.player.get_info()['players']
      display_names = {}
      for p in player_info: display_names[player_info[p]['shipId']] = player_info[p]['name']
      return display_names



