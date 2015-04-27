#
# Overall Agenda page: simple table with one row for each item in the index
#

class Backchannel < React
  def initialize
    @events = nil
  end

  # place a message input field in the buttons area
  def self.buttons()
    return [{button: Message}]
  end

  # render a list of messages
  def render
    _header do
      _h1 'Agenda Backchannel'
    end

    _dl.chatlog Server.backchannel do |message|
      _dt message.user
      _dd message.text
    end
  end

  # on initial load, start listening for events
  def componentDidMount()
    @events = EventSource.new('/events')
    @events.addEventListener :message do |event|
      console.log event
      Server.backchannel << JSON.parse(event.data)
      Main.refresh()
    end
  end

  # terminate HTTP connection
  def componentWillUnmount()
    @events.close() if @events
  end
end
