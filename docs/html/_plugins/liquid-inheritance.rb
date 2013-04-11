require 'liquid_inheritance'

module LiquidInheritance

  class Extends < ::Liquid::Block
    def load_template(context)
      root_path = context.registers[:site].source
      file_path = File.join(root_path, context[@template_name])
      source = File.read(file_path.strip)
      Liquid::Template.parse(source)
    end
  end
end