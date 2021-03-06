#!/usr/bin/env ruby
$LOAD_PATH.unshift File.realpath(File.expand_path('../../../lib', __FILE__))
require 'wunderbar/bootstrap'
require 'whimsy/asf'
require 'whimsy/asf/mlist'

WHITELIST = [
  /^archive-asf-private@cust-asf\.ponee\.io$/,
  /^private@mbox-vm\.apache\.org$/,
  /^security-archive@.*\.apache\.org$/,
]

# ensure that there is a trailing slash (so relative paths will work)
if not ENV['PATH_INFO']
  print "Status: 302 Found\r\nLocation: #{ENV['SCRIPT_URI']}/\r\n\r\n"
  exit
end

# extract information for all security@pmc.apache.org lists
lists = {}
ASF::MLIST.list_parse('sub') do |dom, list, subs|
  next unless list == 'security'
  next unless dom.end_with? '.apache.org'
  lists[dom.sub('.apache.org', '')] = subs
end

_html do
  _whimsy_body(
    title: "Security Mailing List Subscriptions"
  ) do
    path = ENV['PATH_INFO'].sub('/', '')
    if path == ''
      _ul.list_group do
        lists.each do |dom, subs|
          _li.list_group_item do
            _a dom, href: dom
          end
        end
      end

    elsif lists[path]
      podling = ASF::Podling.find(path)
      committee = ASF::Committee.find(path)
      project = ASF::Project.find(path)
      _h2 do
        if podling
          _a podling.display_name, 
            href: "../../roster/ppmc/#{podling.id}"
        else
          _a committee.display_name, 
            href: "../../roster/committee/#{committee.id}"
        end
      end

      _table.table do
        _thead do
          _tr do
            _th 'email'
            _th 'person'
          end
        end

        _tbody do
          lists[path].sort_by {|email| email.downcase}.each do |email|
            person = ASF::Person.find_by_email(email)
            if person
              if person.asf_member? or project.members.include? person
                color = 'bg-success'
              else
                color = 'bg-warning'
              end
            elsif WHITELIST.any? {|regex| email =~ regex}
              color = ''
            else
              color = 'bg-danger'
            end

            _tr class: color do
              _td email
              _td do
                if person
                  if person.asf_member?
                    _b do
                      _a person.public_name, 
                        href: "../../roster/committer/#{person.id}"
                    end
                  else
                    _a person.public_name, 
                      href: "../../roster/committer/#{person.id}"
                  end
                end
              end
            end
          end
        end
      end
    end
  end
end
