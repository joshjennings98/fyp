LIBXML_PKG_CONFIG_CPPFLAGS := $(shell pkg-config --cflags libxml++-2.6)
LIBXML_PKG_CONFIG_LDLIBS := $(shell pkg-config --libs-only-l libxml++-2.6)
LIBXML_PKG_CONFIG_LDFLAGS := $(shell pkg-config --libs-only-L --libs-only-other libxml++-2.6)

CPPFLAGS += -I include -W -Wall -Wno-unused-parameter -Wno-unused-variable
CPPFLAGS += $(LIBXML_PKG_CONFIG_CPPFLAGS)
CPPFLAGS += -Wno-unused-local-typedefs -Wno-unused-function
CPPFLAGS += -I ../../include
CPPFLAGS += -I ../sprovider
CPPFLAGS += -DRAPIDJSON_HAS_STDSTRING=1
CPPFLAGS += -g
#CPPFLAGS += -DNDEBUG=1 
#CPPFLAGS += -O3 -fwhole-program

LDLIBS += $(LIBXML_PKG_CONFIG_LDLIBS) -ltbb -lmetis -ldl
LDFLAGS += $(LIBXML_PKG_CONFIG_LDFLAGS) -pthread

