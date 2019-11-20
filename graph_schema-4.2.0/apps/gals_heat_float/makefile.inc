

$(eval $(call provider_rules_template,gals_heat_float))

define gals_heat_float_instance_template
# $1 = params
# $2 = delta
# $3 = maxsteps
# $4 = filters
# $5 = test : "" or no


demos/gals_heat_float/gals_heat_float_$1.xml : apps/gals_heat_float/create_gals_heat_float_instance.py apps/gals_heat_float/gals_heat_float_graph_type.xml
	mkdir -p $$(dir $$@)
	$$(PYTHON) apps/gals_heat_float/create_gals_heat_float_instance.py  $$(subst _, ,$1) > $$@

ifeq (,$5)
ALL_TEST_XML += demos/gals_heat_float/gals_heat_float_$1.xml
endif

demos/gals_heat_float/gals_heat_float_$1.snap demos/gals_heat_float/gals_heat_float_$1.kv : demos/gals_heat_float/gals_heat_float_$1.xml bin/epoch_sim providers/gals_heat_float.graph.so demos/gals_heat_float/gals_heat_float_$1.checked
	bin/epoch_sim  --log-level 0 --max-steps $3 --snapshots $2 demos/gals_heat_float/gals_heat_float_$1.snap --key-value demos/gals_heat_float/gals_heat_float_$1.kv  demos/gals_heat_float/gals_heat_float_$1.xml

ifeq (,$5)
ALL_gals_heat_float_TESTS += demos/gals_heat_float/gals_heat_float_$1.snap demos/gals_heat_float/gals_heat_float_$1.kv
endif

demos/gals_heat_float/gals_heat_float_$1.mp4 : demos/gals_heat_float/gals_heat_float_$1.xml demos/gals_heat_float/gals_heat_float_$1.snap
	mkdir -p demos/gals_heat_float/gals_heat_float_$1.tmp
	-(cd demos/gals_heat_float/gals_heat_float_$1.tmp && rm *.dot)
	-(cd demos/gals_heat_float/gals_heat_float_$1.tmp && rm *.dot.png)
	-rm demo/gals_heat_float/gals_heat_float_$1.mp4
	$(PYTHON) tools/render_graph_as_dot.py demos/gals_heat_float/gals_heat_float_$1.xml --snapshots demos/gals_heat_float/gals_heat_float_$1.snap --output demos/gals_heat_float/gals_heat_float_$1.tmp/out  \
		$4
	(cd demos/gals_heat_float/gals_heat_float_$1.tmp/  &&  for i in *.dot; do echo $$$$i; neato -Gsize=5,5\! -Gdpi=100 -Tpng $$$$i > $$$$i.png; done )
	#(cd demos/gals_heat_float/gals_heat_float_$1.tmp/  && convert -delay 20 -loop 0 *.dot.png ../gals_heat_float_$1.gif)
	(cd demos/gals_heat_float/gals_heat_float_$1.tmp/  && $(FFMPEG) -r 10 -i out_%06d.dot.png -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" -c:v libx264 -crf 18 ../gals_heat_float_$1.mp4)


ALL_gals_heat_float_DEMOS += demos/gals_heat_float/gals_heat_float_$1.mp4


$(eval $(call softswitch_instance_template,gals_heat_float_$1,demos/gals_heat_float/gals_heat_float_$1.xml,1))
$(eval $(call softswitch_instance_template,gals_heat_float_$1,demos/gals_heat_float/gals_heat_float_$1.xml,4))
$(eval $(call softswitch_instance_template,gals_heat_float_$1,demos/gals_heat_float/gals_heat_float_$1.xml,16))



endef


gals_heat_float_FILTERS_TIME = \
  --bind-dev "*" "state" "timeNow" "color" "blend_colors( (255,255,0), (255,0,255), 0, 10, (value%10))"

gals_heat_float_FILTERS_VALUE = \
  --bind-dev "cell" "state" "v" "color" "heat(-20000000, +20000000, value)"

ifeq ($(NO_APP_TESTS),)


$(eval $(call gals_heat_float_instance_template,4_1000,1,100,$(gals_heat_float_FILTERS_VALUE)))
$(eval $(call gals_heat_float_instance_template,9_1000,1,100,$(gals_heat_float_FILTERS_VALUE)))
$(eval $(call gals_heat_float_instance_template,16_1000,1,100,$(gals_heat_float_FILTERS_TIME)))

#TODO: bring back demos
#$(eval $(call gals_heat_float_instance_template,32,10,10000,$(gals_heat_float_FILTERS_VALUE)))

#$(eval $(call gals_heat_float_instance_template,55,200,100,$(gals_heat_float_FILTERS_VALUE)))

# Needs to be manually rendered with graph_to_field
#$(eval $(call gals_heat_float_instance_template,128,200,50000,$(gals_heat_float_FILTERS_VALUE)))

endif

gals_heat_float_tests : $(ALL_gals_heat_float_TESTS)

gals_heat_float_demos : $(ALL_gals_heat_float_DEMOS)

ALL_TESTS += gals_heat_float_tests

ALL_DEMOS += gals_heat_float_demos


