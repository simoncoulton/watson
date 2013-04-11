module Jekyll
  
  class TitleSortGenerator < Generator
    safe true

    def generate(site)
      site.config['sort_by_module'] = site.posts.sort_by { |a| 
        a.data['module'] ? a.data['module'] : a.data['title'] }
    end

  end

end