import os
import sys
from argparse import ArgumentParser
import math
import time
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def banner():
    console.print("""[bold red]\n
          
        ▄▄▄██████▀▀██████▄▄▄                                An Ext4 File System Parser
    ▄███▀█▄     ▄  ▄     ▄█▀███▄                     Tool to Parse Linux and Android FileSystems
  ██▀█▄████     ████     ████▄█▀██    ███████╗██╗  ██╗████████╗██╗  ██╗    ██████╗  █████╗ ██████╗ ███████╗███████╗██████╗
▄█▀▄███████▄▄ ▄▄████▄▄ ▄▄███████▄▀█▄  ██╔════╝╚██╗██╔╝╚══██╔══╝██║  ██║    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗
██ ██████████████████████████████ ██  █████╗   ╚███╔╝    ██║   ███████║    ██████╔╝███████║██████╔╝███████╗█████╗  ██████╔╝
██ ██████████████████████████████ ██  ██╔══╝   ██╔██╗    ██║   ╚════██║    ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  ██╔══██╗
▀██▀████▀ ▀▀█▀ ▀▀██▀▀ ▀█▀▀ ▀████▀██▀  ███████╗██╔╝ ██╗   ██║        ██║    ██║     ██║  ██║██║  ██║███████║███████╗██║  ██║
  ██▄█▀█▄        ▀▀        ▄█▀█▄██    ╚══════╝╚═╝  ╚═╝   ╚═╝        ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    ▀███▄▄▄              ▄▄▄███▀        A Complete Ext4 File System Parser built by Azr43lKn1ght(Nithin Chenthur Prabhu)
        ▀▀▀██████████████▀▀▀                                   https://github.com/Azr43lKn1ght
                                                                                               
[/bold red]\n""",)

EXT4_BLOCK_SZ       = 4096
EXT4_MIN_BLOCK_SIZE = 1024
EXT4_MAX_BLOCK_SIZE = 65536
# Ext4 Inode
EXT4_BAD_INO            = 1
EXT4_ROOT_INO           = 2
EXT4_BOOT_LOADER_INO    = 5
EXT4_UNDEL_DIR_INO      = 6
EXT4_RESIZE_INO         = 7
EXT4_JOURNAL_INO        = 8
EXT4_GOOD_OLD_FIRST_INO = 11
# Ext4 Super Block
EXT4_SUPER_MAGIC = 0xEF53
EXT4_STATE = {
    'EXT4_VALID_FS'  : 0x0001,
    'EXT4_ERROR_FS'  : 0x0002,
    'EXT4_ORPHAN_FS' : 0x0004
    }

EXT4_ERRORS = {
    'EXT4_ERRORS_CONTINUE' : 1,
    'EXT4_ERRORS_RO'       : 2,
    'EXT4_ERRORS_PANIC'    : 3
    }

EXT4_OS = {
    'EXT4_OS_LINUX'   : 0,
    'EXT4_OS_HURD'    : 1,
    'EXT4_OS_MASIX'   : 2,
    'EXT4_OS_FREEBSD' : 3,
    'EXT4_OS_LITES'   : 4
    }

EXT4_REV_LEVEL = {
    'EXT4_GOOD_OLD_REV' : 0,
    'EXT4_DYNAMIC_REV'  : 1
    }

EXT4_DEF_RESERVED_ID = {
    'EXT4_DEF_RESUID' : 0,
    'EXT4_DEF_RESGID' : 0
    }

EXT4_INODE_NO = {
    'EXT4_BAD_INO'            : 1,
    'EXT4_ROOT_INO'           : 2,
    'EXT4_BOOT_LOADER_INO'    : 5,
    'EXT4_UNDEL_DIR_INO'      : 6,
    'EXT4_RESIZE_INO'         : 7,
    'EXT4_JOURNAL_INO'        : 8,
    'EXT4_GOOD_OLD_FIRST_INO' : 11
    }

EXT4_FEATURE_COMPAT = {
    'EXT4_FEATURE_COMPAT_DIR_PREALLOC'  : 0x0001,
    'EXT4_FEATURE_COMPAT_IMAGIC_INODES' : 0x0002,
    'EXT4_FEATURE_COMPAT_HAS_JOURNAL'   : 0x0004,
    'EXT4_FEATURE_COMPAT_EXT_ATTR'      : 0x0008,
    'EXT4_FEATURE_COMPAT_RESIZE_INODE'  : 0x0010,
    'EXT4_FEATURE_COMPAT_DIR_INDEX'     : 0x0020
    }

EXT4_FEATURE_INCOMPAT = {
    'EXT4_FEATURE_INCOMPAT_COMPRESSION' : 0x0001,
    'EXT4_FEATURE_INCOMPAT_FILETYPE'    : 0x0002,
    'EXT4_FEATURE_INCOMPAT_RECOVER'     : 0x0004,
    'EXT4_FEATURE_INCOMPAT_JOURNAL_DEV' : 0x0008,
    'EXT4_FEATURE_INCOMPAT_META_BG'     : 0x0010,
    'EXT4_FEATURE_INCOMPAT_EXTENTS'     : 0x0040,
    'EXT4_FEATURE_INCOMPAT_64BIT'       : 0x0080,
    'EXT4_FEATURE_INCOMPAT_MMP'         : 0x0100,
    'EXT4_FEATURE_INCOMPAT_FLEX_BG'     : 0x0200,
    'EXT4_FEATURE_INCOMPAT_EA_INODE'    : 0x0400,
    'EXT4_FEATURE_INCOMPAT_DIRDATA'     : 0x1000
    }

EXT4_FEATURE_RO_COMPAT = {
    'EXT4_FEATURE_RO_COMPAT_SPARSE_SUPER' : 0x0001,
    'EXT4_FEATURE_RO_COMPAT_LARGE_FILE'   : 0x0002,
    'EXT4_FEATURE_RO_COMPAT_BTREE_DIR'    : 0x0004,
    'EXT4_FEATURE_RO_COMPAT_HUGE_FILE'    : 0x0008,
    'EXT4_FEATURE_RO_COMPAT_GDT_CSUM'     : 0x0010,
    'EXT4_FEATURE_RO_COMPAT_DIR_NLINK'    : 0x0020,
    'EXT4_FEATURE_RO_COMPAT_EXTRA_ISIZE'  : 0x0040
    }

EXT4_DEFAULT_MOUNT_OPTS = {
    'EXT2_DEFM_DEBUG'          : 0x0001,
    'EXT2_DEFM_BSDGROUPS'      : 0x0002,
    'EXT2_DEFM_XATTR_USER'     : 0x0004,
    'EXT2_DEFM_ACL'            : 0x0008,
    'EXT2_DEFM_UID16'          : 0x0010,
    'EXT3_DEFM_JMODE_DATA'     : 0x0020,
    'EXT3_DEFM_JMODE_ORDERED'  : 0x0040,
    'EXT3_DEFM_JMODE'          : 0x0060,
    'EXT3_DEFM_JMODE_WBACK'    : 0x0060,
    'EXT4_DEFM_NOBARRIER'      : 0x0100,
    'EXT4_DEFM_BLOCK_VALIDITY' : 0x0200,
    'EXT4_DEFM_DISCARD'        : 0x0400,
    'EXT4_DEFM_NODELALLOC'     : 0x0800
    }

EXT4_MISC_FLAGS = {
    'EXT2_FLAGS_SIGNED_HASH'   : 0x0001,
    'EXT2_FLAGS_UNSIGNED_HASH' : 0x0002,
    'EXT2_FLAGS_TEST_FILESYS'  : 0x0004,
    'EXT2_FLAGS_IS_SNAPSHOT'   : 0x0010,
    'EXT2_FLAGS_FIX_SNAPSHOT'  : 0x0020,
    'EXT2_FLAGS_FIX_EXCLUDE'   : 0x0040
    }

# Ext4 Block Group Descriptors
EXT4_BG_FLAGS = {
    'EXT2_BG_INODE_UNINIT' : 0x0001,
    'EXT2_BG_BLOCK_UNINIT' : 0x0002,
    'EXT2_BG_INODE_ZEROED' : 0x0004
    }
# Ext4 Inode Table
EXT4_INODE_ENTRY_SZ = 128
EXT4_NDIR_BLOCKS = 12
EXT4_IND_BLOCK   = EXT4_NDIR_BLOCKS
EXT4_DIND_BLOCK  = EXT4_IND_BLOCK + 1
EXT4_TIND_BLOCK  = EXT4_DIND_BLOCK + 1
EXT4_N_BLOCKS    = EXT4_TIND_BLOCK + 1

EXT4_INODE_MODE = {
    'S_IXOTH' : 0x1,
    'S_IWOTH' : 0x2,
    'S_IROTH' : 0x4,
    'S_IXGRP' : 0x8,
    'S_IWGRP' : 0x10,
    'S_IRGRP' : 0x20,
    'S_IXUSR' : 0x40,
    'S_IWUSR' : 0x80,
    'S_IRUSR' : 0x100,
    'S_ISVTX' : 0x200,
    'S_ISGID' : 0x400,
    'S_ISUID' : 0x800,
    # These are mutually-exclusive file types
    'S_IFIFO'  : 0x1000,
    'S_IFCHR'  : 0x2000,
    'S_IFDIR'  : 0x4000,
    'S_IFBLK'  : 0x6000,
    'S_IFREG'  : 0x8000,
    'S_IFLNK'  : 0xA000,
    'S_IFSOCK' : 0xC000
    }

EXT4_INODE_FLAGS = {
    'EXT4_SECRM_FL'             : 0x1, 
    'EXT4_UNRM_FL'              : 0x2,  
    'EXT4_COMPR_FL'             : 0x4,  
    'EXT4_SYNC_FL'              : 0x8,  
    'EXT4_IMMUTABLE_FL'         : 0x10, 
    'EXT4_APPEND_FL'            : 0x20,  
    'EXT4_NODUMP_FL'            : 0x40,  
    'EXT4_NOATIME_FL'           : 0x80,  
    'EXT4_DIRTY_FL'             : 0x100,  
    'EXT4_COMPRBLK_FL'          : 0x200,  
    'EXT4_NOCOMPR_FL'           : 0x400,  
    'EXT4_ECOMPR_FL'            : 0x800,  
    'EXT4_INDEX_FL'             : 0x1000,  
    'EXT4_IMAGIC_FL'            : 0x2000,  
    'EXT4_JOURNAL_DATA_FL'      : 0x4000,  
    'EXT4_NOTAIL_FL'            : 0x8000,  
    'EXT4_DIRSYNC_FL'           : 0x10000,  
    'EXT4_TOPDIR_FL'            : 0x20000,  
    'EXT4_HUGE_FILE_FL'         : 0x40000,  
    'EXT4_EXTENTS_FL'           : 0x80000, 
    'EXT4_EA_INODE_FL'          : 0x200000,  
    'EXT4_EOFBLOCKS_FL'         : 0x400000,  
    'EXT4_RESERVED_FL'          : 0x80000000,  
    # Aggregate flags
    'EXT4_FL_USER_VISIBLE'      : 0x4BDFFF, 
    'EXT4_FL_USER_MODIFIABLE'   : 0x4B80FF,  
    }
# Ext4 Extent Tree
EXT4_EXTENT_TREE_MAGIC = 0xF30A
# Ext4 Directory Entries
EXT4_NAME_LEN = 255
EXT4_HTREE_NAME_LEN = 4
#for hash tree directory resolution
EXT4_FILE_TYPE = {
    'EXT4_FT_UNKNOWN'  : 0x0,
    'EXT4_FT_REG_FILE' : 0x1,
    'EXT4_FT_DIR'      : 0x2,
    'EXT4_FT_CHRDEV'   : 0x3,
    'EXT4_FT_BLKDEV'   : 0x4,
    'EXT4_FT_FIFO'     : 0x5,
    'EXT4_FT_SOCK'     : 0x6,
    'EXT4_FT_SYMLINK'  : 0x7
    }
# Ext4 Extended Attributes
EXT4_XATTR_MAGIC = 0xEA020000
# Journal will be implemented in next version
# Ext4 Journal, jbd2
EXT4_JNL_BACKUP_BLOCKS = 1
JBD2_MAGIC_NUMBER = 0xC03B3998
# JBD2_CHECKSUM_BYTES = (32 / sizeof(u32))
JBD2_CHECKSUM_BYTES = (32 / 4)

EXT4_JNL_BLOCK_TYPE = {
    'JBD2_DESCRIPTOR_BLOCK'    : 1,
    'JBD2_COMMIT_BLOCK'        : 2,
    'JBD2_SUPERBLOCK_V1'       : 3,
    'JBD2_SUPERBLOCK_V2'       : 4,
    'JBD2_REVOKE_BLOCK'        : 5
    }

EXT4_JNL_FEATURE_COMPAT = {
    'JBD2_FEATURE_COMPAT_CHECKSUM' : 0x00000001
    }

EXT4_JNL_FEATURE_INCOMPAT = {
    'JBD2_FEATURE_INCOMPAT_REVOKE'       : 0x00000001,
    'JBD2_FEATURE_INCOMPAT_64BIT'        : 0x00000002,
    'JBD2_FEATURE_INCOMPAT_ASYNC_COMMIT' : 0x00000004
    }

EXT4_JNL_FLAGS = {
    'JBD2_FLAG_ESCAPE'    : 1,
    'JBD2_FLAG_SAME_UUID' : 2,
    'JBD2_FLAG_DELETED'   : 4,
    'JBD2_FLAG_LAST_TAG'  : 8
    }

EXT4_JNL_CHKSUM_TYPE = {
    'JBD2_CRC32_CHKSUM' : 1,
    'JBD2_MD5_CHKSUM'   : 2,
    'JBD2_SHA1_CHKSUM'  : 3
    }
No_of_block_in_a_group = 32768
size_of_each_block_group = 134217728
#
# Ext4 Hash
#
EXT4_HASH_VERSION = {
    'DX_HASH_LEGACY'            : 0x0,
    'DX_HASH_HALF_MD4'          : 0x1,
    'DX_HASH_TEA'               : 0x2,
    'DX_HASH_LEGACY_UNSIGNED'   : 0x3,
    'DX_HASH_HALF_MD4_UNSIGNED' : 0x4,
    'DX_HASH_TEA_UNSIGNED'      : 0x5
    }

def timestamp_to_utc_string(timestamp):
    time_struct = time.gmtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', time_struct)

class Ext4Parser:
    def __init__(self, filepath):
        self.console = Console()
        # self.filepath = filepath
        # self.filepath = filepath
        
        self.filepath = filepath
        file_size = Path(filepath).stat().st_size 
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold green]Reading file..."),
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Loading...", total=file_size)

            with open(filepath, "rb") as f:
                self.f = f.read()  # Read the entire file

                # Complete the task once file is fully read
                progress.update(task, advance=file_size)
                console.print("[bold green]File read successfully![/bold green]")

        # print(f"File {filepath} read successfully. Total size: {len(self.f)} bytes")
               
        self.ext4_superblock = {
            'sb_inodes_count'           : 0,
            'sb_blocks_count_lo'        : 0,
            'sb_r_blocks_count_lo'      : 0,  
            'sb_free_blocks_count_lo'   : 0,  
            'sb_free_inodes_count'      : 0, 
            'sb_first_data_block'       : 0,  
            'sb_log_block_size'         : 0,  
            'sb_obso_log_frag_size'     : 0,  
            'sb_blocks_per_group'       : 0,  
            'sb_obso_frags_per_group'   : 0,  
            'sb_inodes_per_group'       : 0,  
            'sb_mtime'                  : 0, 
            'sb_wtime'                  : 0,  
            'sb_mnt_count'              : 0,  
            'sb_max_mnt_count'          : 0xFFFF, 
            'sb_magic'                  : EXT4_SUPER_MAGIC,  
            'sb_state'                  : EXT4_STATE['EXT4_VALID_FS'], 
            'sb_errors'                 : EXT4_ERRORS['EXT4_ERRORS_RO'], 
            'sb_minor_rev_level'        : 0, 
            'sb_lastcheck'              : 0, 
            'sb_checkinterval'          : 0,  
            'sb_creator_os'             : EXT4_OS['EXT4_OS_LINUX'], 
            'sb_rev_level'              : EXT4_REV_LEVEL['EXT4_DYNAMIC_REV'], 
            'sb_def_resuid'             : EXT4_DEF_RESERVED_ID['EXT4_DEF_RESUID'], 
            'sb_def_resgid'             : EXT4_DEF_RESERVED_ID['EXT4_DEF_RESGID'], 
            #if EXT4_DYNAMIC_REV superblocks
            'sb_first_ino'              : EXT4_INODE_NO['EXT4_GOOD_OLD_FIRST_INO'],
            'sb_inode_size'             : 0, 
            'sb_block_group_nr'         : 0, 
            'sb_feature_compat'         : 0,  
            'sb_feature_incompat'       : 0,  
            'sb_feature_ro_compat'      : 0, 
            'sb_uuid'                   : 0, 
            'sb_volume_name'            : "", 
            'sb_last_mounted'           : "", 
            'sb_algorithm_usage_bitmap' : 0, 
            'sb_prealloc_blocks'         : 0,  
            'sb_prealloc_dir_blocks'     : 0,  
            'sb_reserved_gdt_blocks'     : 0,
            # Journaling if EXT4_FEATURE_COMPAT_HAS_JOURNAL
            'sb_journal_uuid'            : 0,  
            'sb_journal_inum'            : EXT4_INODE_NO['EXT4_JOURNAL_INO'], 
            'sb_journal_dev'             : 0,  
            'sb_last_orphan'             : 0,  
            'sb_hash_seed'               : 0,  
            'sb_def_hash_version'        : EXT4_HASH_VERSION['DX_HASH_TEA'], 
            'sb_reserved_char_pad'       : EXT4_JNL_BACKUP_BLOCKS,  
            'sb_desc_size'               : 0, 
            'sb_default_mount_opts'      : 0x0000,  
            'sb_first_meta_bg'           : 0, 
            'sb_mkfs_time'               : 0,  
            'sb_jnl_blocks'              : 0,
            #EXT4_FEATURE_INCOMPAT_64BIT 
            'sb_blocks_count_hi'         : 0,  
            'sb_r_blocks_count_hi'       : 0,  
            'sb_free_blocks_count_hi'    : 0,  
            'sb_min_extra_isize'         : 0,  
            'sb_want_extra_isize'        : 0,  
            'sb_flags'                   : 0x0000,  
            'sb_raid_stride'             : 0,     
            'sb_mmp_interval'            : 0,  
            'sb_mmp_block'               : 0,  
            'sb_raid_stripe_width'       : 0,  
            'sb_log_groups_per_flex'     : 0,  
            'sb_reserved_char_pad2'      : 0,  
            'sb_reserved_pad'            : 0,  
            'sb_kbytes_written'          : 0,  
            'sb_reserved'                : 0,  
    
            }
        
        self.ext4_blockgroupdescriptor = {
            'bg_block_bitmap_lo'         : 0, 
            'bg_inode_bitmap_lo'         : 0,  
            'bg_inode_table_lo'          : 0,  
            'bg_free_blocks_count_lo'    : 0,  
            'bg_free_inodes_count_lo'    : 0,  
            'bg_used_dirs_count_lo'      : 0,  
            'bg_flags'                   : EXT4_BG_FLAGS['EXT2_BG_INODE_UNINIT'],  
            'bg_exclude_bitmap_lo'       : 0,  
            'bg_reserved1'               : 0,  
            'bg_itable_unused_lo'        : 0,  
            'bg_checksum'                : 0,  
            #if EXT4_FEATURE_INCOMPAT_64BIT and 'sb_desc_size' > 32
            'bg_block_bitmap_hi'         : 0, 
            'bg_inode_bitmap_hi'         : 0, 
            'bg_inode_table_hi'          : 0, 
            'bg_free_blocks_count_hi'    : 0, 
            'bg_free_inodes_count_hi'    : 0, 
            'bg_used_dirs_count_hi'      : 0, 
            'bg_itable_unused_hi'        : 0, 
            'bg_exclude_bitmap_hi'       : 0, 
            'bg_reserved2'               : 0, 
            'bg_reserved3'               : 0, 
                 }
        self.maxinode=0
        self.ext4_inode = {
            'i_mode'                     : EXT4_INODE_MODE['S_IXOTH'],
            'i_uid'                      : 0,  
            'i_size_lo'                  : 0,  
            'i_atime'                    : 0,  
            'i_ctime'                    : 0,  
            'i_mtime'                    : 0,  
            'i_dtime'                    : 0,  
            'i_gid'                      : 0,  
            'i_links_count'              : 0,  
            'i_blocks_lo'                : 0,  
            'i_flags'                    : EXT4_INODE_FLAGS['EXT4_SECRM_FL'],
            'l_i_version'                : 0,  
            'i_block'                    : 0,  
            'i_generation'               : 0,  
            'i_file_acl_lo'              : 0,  
            'i_size_high'                : 0,  
            'i_obso_faddr'               : 0,  
            'l_i_blocks_high'            : 0,  
            'l_i_file_acl_high'          : 0,  
            'l_i_uid_high'               : 0,  
            'l_i_gid_high'               : 0,  
            'l_i_reserved2'              : 0,  
            'i_extra_isize'              : 0,  
            'i_pad1'                     : 0,  
            'i_ctime_extra'              : 0,  
            'i_mtime_extra'              : 0,  
            'i_atime_extra'              : 0,  
            'i_crtime'                   : 0,  
            'i_crtime_extra'             : 0,  
            'i_version_hi'               : 0,
            'i_projid'                   : 0,
            'i_reserved'                 : 0,
            }
        
        self.ext4_extent_header = {
            'eh_magic'                   : EXT4_EXTENT_TREE_MAGIC,
            'eh_entries'                 : 0, 
            'eh_max'                     : 0, 
            'eh_depth'                   : 0, # if 0,this extent node points to data blocks, otherwise, this extent node points to other extent nodes
            'eh_generation'              : 0,
            }
            
        self.ext4_extent_header_copy = {
            'eh_magic'                   : EXT4_EXTENT_TREE_MAGIC,
            'eh_entries'                 : 0, 
            'eh_max'                     : 0, 
            'eh_depth'                   : 0, # if 0,this extent node points to data blocks, otherwise, this extent node points to other extent nodes
            'eh_generation'              : 0,
            }
        
        self.ext4_extent = {
            'ee_block'                   : 0,
            'ee_len'                     : 0,
            'ee_start_hi'                : 0,
            'ee_start_lo'                : 0,
            }
        
        self.ext4_extent_copy = {
            'ee_block'                   : 0,
            'ee_len'                     : 0,
            'ee_start_hi'                : 0,
            'ee_start_lo'                : 0,
            }
        
        self.ext4_extent_idx = {
            'ei_block'                   : 0, 
            'ei_leaf_lo'                 : 0,                                               
            'ei_leaf_hi'                 : 0, 
            'ei_unused'                  : 0, 
            }

        self.ext4_extent_idx_copy = {
            'ei_block'                   : 0, 
            'ei_leaf_lo'                 : 0,                                               
            'ei_leaf_hi'                 : 0, 
            'ei_unused'                  : 0, 
            }
        
        self.ext4_dir_entry = {
            'inode'                      : 0,  
            'rec_len'                    : 0,  
            'name_len'                   : 0,  
            'name'                       : "", 
        }
        
        self.ext4_dir_entry_2 = {
            'inode'                      : 0,  
            'rec_len'                    : 0,  
            'name_len'                   : 0,  
            'file_type'                  : EXT4_FILE_TYPE['EXT4_FT_UNKNOWN'],
            'name'                       : "",
            }
        
        self.dx_root = {
            'dot_inode'                  : 0,  
            'dot_rec_len'                : 0,  
            'dot_name_len'               : 0,  
            'dot_file_type'              : 0,  
            'dot_name'                   : "", 
            'dot_dot_inode'              : 0,  
            'dot_dot_rec_len'            : 0,  
            'dot_dot_name_len'           : 0,  
            'dot_dot_file_type'          : 0,  
            'dot_dot_name'               : "", 
            'reserved_zero'              : 0,  
            'hash_version'               : EXT4_HASH_VERSION['DX_HASH_LEGACY'],
            'info_length'                : 0, 
            'indirect_levels'            : 0, 
            'unused_flags'               : 0, 
            'limit'                      : 0, 
            'count'                      : 0, 
            'block'                      : 0, 
            'entries'                    : 0, 
            }
        
        self.dx_node = {
            'fake_inode'                 : 0,  
            'fake_rec_len'               : 0,  
            'fake_name_len'              : 0,  
            'fake_file_type'             : 0,  
            'limit'                      : 0,  
            'count'                      : 0,  
            'block'                      : 0,  
            'entries'                    : 0,  
            }
        
        self.dx_entry = {
            'hash'                       : 0,  
            'block'                      : 0,  
            }
        
        self.ext4_xattr_header = {
            'xh_magic'                   : EXT4_XATTR_MAGIC,  
            'xh_refcount'                : 0,  
            'xh_blocks'                  : 0,  
            'xh_hash'                    : 0,  
            'xh_reserved'                : 0,  
            }
        
        self.ext4_xattr_entry = {
            'xe_name_len'                : 0,  
            'xe_name_index'              : 0,  
            'xe_value_offs'              : 0,                                    
            'xe_value_block'             : 0,                                  
            'xe_value_size'              : 0,  
            'xe_hash'                    : 0,  
            'xe_name'                    : "", 
            }

            
        self.DEBUG = False
        
    def str2int_le(self, str_list):
        return int.from_bytes(str_list.encode(), byteorder='little')

    def parse_ext4(self):
        offset = 0
        offset = offset+1024 # Superblock is at 1024 bytes
        self.parse_ext4_superblock(offset)
        # exit()
        offset = offset + 1024 #end of superblock
        offset = offset + 2048 #start of block group descriptor and end of free space
        # count_of_blocks = self.ext4_superblock['sb_blocks_count_lo']
        # bg_num =math.ceil((count_of_blocks - self.ext4_superblock['sb_first_data_block']) / self.ext4_superblock['sb_blocks_per_group'])
        # print(f"Total Block Groups: {bg_num}")
        count_of_bg=math.ceil(self.ext4_superblock['sb_blocks_count_lo']/self.ext4_superblock['sb_blocks_per_group'])
        print(f"Total Block Groups: {count_of_bg}")
        # exit()
        og_offset=offset
        self.maxinode=self.ext4_superblock['sb_inodes_count']
        for i in range(count_of_bg):
            print(f"\n\nParsing Block Group {i}:\n\n")
            self.parse_ext4_block_group_descriptor(og_offset)
            if self.ext4_superblock['sb_desc_size'] == 32:
                # print("Azr43l")
                # exit()
                og_offset = og_offset + 32
            else:
                og_offset = og_offset + 64
        # if self.ext4_superblock['sb_feature_ro_compat'] & EXT4_FEATURE_RO_COMPAT['EXT4_FEATURE_RO_COMPAT_SPARSE_SUPER']:
        #     offset=offset + 32 * count_of_bg
        # else:
        #     offset = offset + 64 * count_of_bg
        # print(f"End of Block Group Descriptor Table: {hex(offset)}")
        # print("OFFSET: ",hex(og_offset))
        # exit()
        for i in range(count_of_bg):
            print(f"\n\nParsing Inode Table for Block Group {i}:\n\n")
            current_bg_offset = int.from_bytes(self.f[offset+8:offset+12], byteorder='little')
            inode_table_offset=current_bg_offset*EXT4_BLOCK_SZ
            # print(f"Offset of Inode Table: {hex(inode_table_offset)}")
            # print("offset",hex(offset))
            self.parse_ext4_inode_table(inode_table_offset,i)
            if self.ext4_superblock['sb_desc_size'] == 32:
                # print("Azr43l")
                # exit()
                offset=offset + 32
            else:
                offset = offset + 64
        # print(f"End of Inode Table: {hex(offset)}")
   
    def parse_ext4_superblock(self,offset):
        self.ext4_superblock['sb_inodes_count'] = int.from_bytes(self.f[offset+0x00:offset+0x04], byteorder='little')
        print(f"Total Inodes: {self.ext4_superblock['sb_inodes_count']}")
        self.ext4_superblock['sb_blocks_count_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
        print(f"Total Blocks: {self.ext4_superblock['sb_blocks_count_lo']}")
        self.ext4_superblock['sb_r_blocks_count_lo'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Reserved Blocks: {self.ext4_superblock['sb_r_blocks_count_lo']}")
        self.ext4_superblock['sb_free_blocks_count_lo'] = int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
        print(f"Free Blocks: {self.ext4_superblock['sb_free_blocks_count_lo']}")
        self.ext4_superblock['sb_free_inodes_count'] = int.from_bytes(self.f[offset+0x10:offset+0x14], byteorder='little')
        print(f"Free Inodes: {self.ext4_superblock['sb_free_inodes_count']}")
        self.ext4_superblock['sb_first_data_block'] = int.from_bytes(self.f[offset+0x14:offset+0x18], byteorder='little')
        print(f"First Data Block: {self.ext4_superblock['sb_first_data_block']}")
        self.ext4_superblock['sb_log_block_size'] = int.from_bytes(self.f[offset+0x18:offset+0x1C], byteorder='little')
        print(f"Log Block Size: {self.ext4_superblock['sb_log_block_size']}")
        self.ext4_superblock['sb_obso_log_frag_size'] = int.from_bytes(self.f[offset+0x1C:offset+0x20], byteorder='little')
        print(f"Obsolete Log Fragment Size: {self.ext4_superblock['sb_obso_log_frag_size']}")
        self.ext4_superblock['sb_blocks_per_group'] = int.from_bytes(self.f[offset+0x20:offset+0x24], byteorder='little')
        print(f"Blocks per Group: {self.ext4_superblock['sb_blocks_per_group']}")
        self.ext4_superblock['sb_obso_frags_per_group'] = int.from_bytes(self.f[offset+0x24:offset+0x28], byteorder='little')
        print(f"Obsolete Fragments per Group: {self.ext4_superblock['sb_obso_frags_per_group']}")
        self.ext4_superblock['sb_inodes_per_group'] = int.from_bytes(self.f[offset+0x28:offset+0x2C], byteorder='little')
        print(f"Inodes per Group: {self.ext4_superblock['sb_inodes_per_group']}")
        self.ext4_superblock['sb_mtime'] = int.from_bytes(self.f[offset+0x2C:offset+0x30], byteorder='little')
        print(f"Mount Time: {datetime.utcfromtimestamp(self.ext4_superblock['sb_mtime']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_superblock['sb_wtime'] = int.from_bytes(self.f[offset+0x30:offset+0x34], byteorder='little')
        print(f"Write Time: {datetime.utcfromtimestamp(self.ext4_superblock['sb_wtime']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_superblock['sb_mnt_count'] = int.from_bytes(self.f[offset+0x34:offset+0x36], byteorder='little')
        print(f"Mount Count: {self.ext4_superblock['sb_mnt_count']}")
        self.ext4_superblock['sb_max_mnt_count'] = int.from_bytes(self.f[offset+0x36:offset+0x38], byteorder='little')
        print(f"Max Mount Count: {self.ext4_superblock['sb_max_mnt_count']}")
        self.ext4_superblock['sb_magic'] = int.from_bytes(self.f[offset+0x38:offset+0x3A], byteorder='little')
        print(f"Magic Number: {self.ext4_superblock['sb_magic']}")
        self.ext4_superblock['sb_state'] = int.from_bytes(self.f[offset+0x3A:offset+0x3C], byteorder='little')
        state = ""
        if self.ext4_superblock['sb_state'] == 1:
            state = "Valid FS"
        elif self.ext4_superblock['sb_state'] == 2:
            state = "Error FS"
        elif self.ext4_superblock['sb_state'] == 4:
            state = "Orphan FS"
        print(f"State: {state}")
        self.ext4_superblock['sb_errors'] = int.from_bytes(self.f[offset+0x3C:offset+0x3E], byteorder='little')
        errors = ""
        if self.ext4_superblock['sb_errors'] == 1:
            errors = "Continue"
        elif self.ext4_superblock['sb_errors'] == 2:
            errors = "Read-Only"
        elif self.ext4_superblock['sb_errors'] == 3:
            errors = "Panic"
        print(f"Errors: {errors}")
        self.ext4_superblock['sb_minor_rev_level'] = int.from_bytes(self.f[offset+0x3E:offset+0x40], byteorder='little')
        print(f"Minor Revision Level: {self.ext4_superblock['sb_minor_rev_level']}")
        self.ext4_superblock['sb_lastcheck'] = int.from_bytes(self.f[offset+0x40:offset+0x44], byteorder='little')
        print(f"Last Check: {datetime.utcfromtimestamp(self.ext4_superblock['sb_lastcheck']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_superblock['sb_checkinterval'] = int.from_bytes(self.f[offset+0x44:offset+0x48], byteorder='little')
        print(f"Check Interval: {self.ext4_superblock['sb_checkinterval']}")
        self.ext4_superblock['sb_creator_os'] = int.from_bytes(self.f[offset+0x48:offset+0x4C], byteorder='little')
        creator_os = ""
        if self.ext4_superblock['sb_creator_os'] == 0:
            creator_os = "Linux"
        elif self.ext4_superblock['sb_creator_os'] == 1:
            creator_os = "Hurd"
        elif self.ext4_superblock['sb_creator_os'] == 2:
            creator_os = "Masix"
        elif self.ext4_superblock['sb_creator_os'] == 3:
            creator_os = "FreeBSD"
        elif self.ext4_superblock['sb_creator_os'] == 4:
            creator_os = "Lites"
        print(f"Creator OS: {creator_os}")
        self.ext4_superblock['sb_rev_level'] = int.from_bytes(self.f[offset+0x4C:offset+0x50], byteorder='little')
        rev_level = ""
        if self.ext4_superblock['sb_rev_level'] == 0:
            rev_level = "Good Old Rev"
        elif self.ext4_superblock['sb_rev_level'] == 1:
            rev_level = "Dynamic Rev"
        print(f"Revision Level: {rev_level}")
        self.ext4_superblock['sb_def_resuid'] = int.from_bytes(self.f[offset+0x50:offset+0x52], byteorder='little')
        print(f"Default Reserved UID: {self.ext4_superblock['sb_def_resuid']}")
        self.ext4_superblock['sb_def_resgid'] = int.from_bytes(self.f[offset+0x52:offset+0x54], byteorder='little')
        print(f"Default Reserved GID: {self.ext4_superblock['sb_def_resgid']}")
        print("\n\nFor EXT4_DYNAMIC_REV Super Blocks Only\n\n")
        self.ext4_superblock['sb_first_ino'] = int.from_bytes(self.f[offset+0x54:offset+0x58], byteorder='little')
        print(f"First Inode: {self.ext4_superblock['sb_first_ino']}")
        self.ext4_superblock['sb_inode_size'] = int.from_bytes(self.f[offset+0x58:offset+0x5A], byteorder='little')
        print(f"Inode Size: {self.ext4_superblock['sb_inode_size']}")
        self.ext4_superblock['sb_block_group_nr'] = int.from_bytes(self.f[offset+0x5A:offset+0x5C], byteorder='little')
        print(f"Block Group Number: {self.ext4_superblock['sb_block_group_nr']}")
        self.ext4_superblock['sb_feature_compat'] = int.from_bytes(self.f[offset+0x5C:offset+0x60], byteorder='little')
        feature_compat = ""
        if self.ext4_superblock['sb_feature_compat'] & 0x0001:
            feature_compat += " Directory Preallocation "
        if self.ext4_superblock['sb_feature_compat'] & 0x0002:
            feature_compat += " Imagic Inodes "
        if self.ext4_superblock['sb_feature_compat'] & 0x0004:
            feature_compat += " Has Journal "
        if self.ext4_superblock['sb_feature_compat'] & 0x0008:
            feature_compat += " Extended Attributes "
        if self.ext4_superblock['sb_feature_compat'] & 0x0010:
            feature_compat += " Resize Inode "
        if self.ext4_superblock['sb_feature_compat'] & 0x0020:
            feature_compat += " Directory Index "
        print("Compatible feature: " + feature_compat)
        self.ext4_superblock['sb_feature_incompat'] = int.from_bytes(self.f[offset+0x60:offset+0x64], byteorder='little')
        feature_incompat = ""
        if self.ext4_superblock['sb_feature_incompat'] & 0x0001:
            feature_incompat += " Compression"
        if self.ext4_superblock['sb_feature_incompat'] & 0x0002:
            feature_incompat += " Filetype "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0004:
            feature_incompat += " Recover "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0008:
            feature_incompat += " Journal_Device "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0010:
            feature_incompat += " Meta_Block_Group "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0040:
            feature_incompat += " Extents "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0080:
            feature_incompat += " 64-bit "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0100:
            feature_incompat += " MMP "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0200:
            feature_incompat += " Flex_Block_Group "
        if self.ext4_superblock['sb_feature_incompat'] & 0x0400:
            feature_incompat += " EA_Inode "
        if self.ext4_superblock['sb_feature_incompat'] & 0x1000:
            feature_incompat += " Directory_Data "
        if self.ext4_superblock['sb_feature_incompat'] & 0x2000:
            feature_incompat += " Reserved "
        if self.ext4_superblock['sb_feature_incompat'] & 0x4000:
            feature_incompat += " Snapshot "
        if self.ext4_superblock['sb_feature_incompat'] & 0x8000:
            feature_incompat += " Snapshot_Quota "
        if self.ext4_superblock['sb_feature_incompat'] & 0x10000:
            feature_incompat += " Encrypted "
        if self.ext4_superblock['sb_feature_incompat'] & 0x20000:
            feature_incompat += " Casefold "
        print("Incompatible feature: " + feature_incompat)
        self.ext4_superblock['sb_feature_ro_compat'] = int.from_bytes(self.f[offset+0x64:offset+0x68], byteorder='little')
        feature_ro_compat = ""
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0001:
            feature_ro_compat += " Sparse_Super "
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0002:
            feature_ro_compat += " Large_File "
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0004:
            feature_ro_compat += " Btree_Directory "
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0008:
            feature_ro_compat += " Huge_File "
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0010:
            feature_ro_compat += " GDT_CSUM "
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0020:
            feature_ro_compat += " Directory_NLink "
        if self.ext4_superblock['sb_feature_ro_compat'] & 0x0040:
            feature_ro_compat += " Extra_ISize "
        print("Read-Only Compatible feature: " + feature_ro_compat)
        self.ext4_superblock['sb_uuid'] = self.f[offset+0x68:offset+0x78].hex()
        formatted_uuid = ' '.join(self.ext4_superblock['sb_uuid'][i:i+2] for i in range(0, len(self.ext4_superblock['sb_uuid']), 2))
        print(f"UUID: {formatted_uuid}")
        self.ext4_superblock['sb_volume_name'] = self.f[offset+0x78:offset+0x88].decode('utf-8').rstrip('\x00')
        print(f"Volume Name: {self.ext4_superblock['sb_volume_name']}")
        self.ext4_superblock['sb_last_mounted'] = self.f[offset+0x88:offset+0xc8].decode('utf-8').rstrip('\x00')
        print(f"Last Mounted: {self.ext4_superblock['sb_last_mounted']}")
        self.ext4_superblock['sb_algorithm_usage_bitmap'] = int.from_bytes(self.f[offset+0xC8:offset+0xCC], byteorder='little')
        print(f"Algorithm Usage Bitmap: {self.ext4_superblock['sb_algorithm_usage_bitmap']}")
        self.ext4_superblock['sb_prealloc_blocks'] = int.from_bytes(self.f[offset+0xCC:offset+0xCD], byteorder='little')
        print("\n\nEXT4_FEATURE_COMPAT_DIR_PREALLOC on for performance hints Directory preallocation\n\n")
        print(f"Preallocated Blocks: {self.ext4_superblock['sb_prealloc_blocks']}")
        self.ext4_superblock['sb_prealloc_dir_blocks'] = int.from_bytes(self.f[offset+0xCD:offset+0xCE], byteorder='little')
        print(f"Preallocated Directory Blocks: {self.ext4_superblock['sb_prealloc_dir_blocks']}")
        self.ext4_superblock['sb_reserved_gdt_blocks'] = int.from_bytes(self.f[offset+0xCE:offset+0xD0], byteorder='little')
        print(f"Reserved GDT Blocks: {self.ext4_superblock['sb_reserved_gdt_blocks']}")
        print("\n\nFor EXT4_FEATURE_COMPAT_HAS_JOURNAL Only\n\n")
        self.ext4_superblock['sb_journal_uuid'] = self.f[offset+0xD0:offset+0xE0].hex()
        formatted_journal_uuid = ' '.join(self.ext4_superblock['sb_journal_uuid'][i:i+2] for i in range(0, len(self.ext4_superblock['sb_journal_uuid']), 2))
        print(f"Journal UUID: {formatted_journal_uuid}")
        self.ext4_superblock['sb_journal_inum'] = int.from_bytes(self.f[offset+0xE0:offset+0xE4], byteorder='little')
        print(f"Journal Inode: {self.ext4_superblock['sb_journal_inum']}")
        self.ext4_superblock['sb_journal_dev'] = int.from_bytes(self.f[offset+0xE4:offset+0xE8], byteorder='little')
        print(f"Journal Device: {self.ext4_superblock['sb_journal_dev']}")
        self.ext4_superblock['sb_last_orphan'] = int.from_bytes(self.f[offset+0xE8:offset+0xEC], byteorder='little')
        print(f"Last Orphan: {self.ext4_superblock['sb_last_orphan']}")
        self.ext4_superblock['sb_hash_seed'] = int.from_bytes(self.f[offset+0xEC:offset+0xFC], byteorder='little')
        print(f"HTREE Hash Seed: {self.ext4_superblock['sb_hash_seed']}")
        self.ext4_superblock['sb_def_hash_version'] = int.from_bytes(self.f[offset+0xFC:offset+0xFD], byteorder='little')
        def_hashversion = ""
        if self.ext4_superblock['sb_def_hash_version'] == 0:
            def_hashversion = "Legacy"
        elif self.ext4_superblock['sb_def_hash_version'] == 1:
            def_hashversion = "Half MD4"
        elif self.ext4_superblock['sb_def_hash_version'] == 2:
            def_hashversion = "TEA"
        elif self.ext4_superblock['sb_def_hash_version'] == 3:
            def_hashversion = "Legacy Unsigned"
        elif self.ext4_superblock['sb_def_hash_version'] == 4:
            def_hashversion = "Half MD4 Unsigned"
        elif self.ext4_superblock['sb_def_hash_version'] == 5:
            def_hashversion = "TEA Unsigned"
        print(f"Default Hash Version: {def_hashversion}")
        self.ext4_superblock['sb_reserved_char_pad'] = int.from_bytes(self.f[offset+0xFD:offset+0xFE], byteorder='little')
        print(f"Reserved Char Pad: {self.ext4_superblock['sb_reserved_char_pad']}")
        self.ext4_superblock['sb_desc_size'] = int.from_bytes(self.f[offset+0xFE:offset+0x100], byteorder='little')
        print(f"Descriptor Size: {self.ext4_superblock['sb_desc_size']}")
        self.ext4_superblock['sb_default_mount_opts'] = int.from_bytes(self.f[offset+0x100:offset+0x104], byteorder='little')
        default_mount_opts = ""
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0001:
            default_mount_opts += " Debug "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0002:
            default_mount_opts += " BSD Groups "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0004:
            default_mount_opts += " XATTR User "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0008:
            default_mount_opts += " ACL "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0010:
            default_mount_opts += " UID16 "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0020:
            default_mount_opts += " JMODE Data "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0040:
            default_mount_opts += " JMODE Ordered "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0060:
            default_mount_opts += " JMODE "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0100:
            default_mount_opts += " No Barrier "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0200:
            default_mount_opts += " Block Validity "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0400:
            default_mount_opts += " Discard "
        if self.ext4_superblock['sb_default_mount_opts'] & 0x0800:
            default_mount_opts += " No Delayed Allocation "
        print(f"Default Mount Options: {default_mount_opts}")
        self.ext4_superblock['sb_first_meta_bg'] = int.from_bytes(self.f[offset+0x104:offset+0x108], byteorder='little')
        print(f"First Meta Block Group: {self.ext4_superblock['sb_first_meta_bg']}")
        self.ext4_superblock['sb_mkfs_time'] = int.from_bytes(self.f[offset+0x108:offset+0x10C], byteorder='little')
        print(f"MKFS Time: {datetime.utcfromtimestamp(self.ext4_superblock['sb_mkfs_time']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_superblock['sb_jnl_blocks'] = int.from_bytes(self.f[offset+0x108:offset+0x150], byteorder='little')
        # print(f"Journal Backup: {self.ext4_superblock['sb_jnl_blocks']}")
        self.ext4_superblock['sb_blocks_count_hi'] = int.from_bytes(self.f[offset+0x150:offset+0x154], byteorder='little')
        self.ext4_superblock['sb_r_blocks_count_hi'] = int.from_bytes(self.f[offset+0x154:offset+0x158], byteorder='little')
        self.ext4_superblock['sb_free_blocks_count_hi'] = int.from_bytes(self.f[offset+0x158:offset+0x15C], byteorder='little')
        self.ext4_superblock['sb_min_extra_isize'] = int.from_bytes(self.f[offset+0x15C:offset+0x15E], byteorder='little')
        self.ext4_superblock['sb_want_extra_isize'] = int.from_bytes(self.f[offset+0x15E:offset+0x160], byteorder='little')
        self.ext4_superblock['sb_flags'] = int.from_bytes(self.f[offset+0x160:offset+0x164], byteorder='little')
        miscflags = ""
        if self.ext4_superblock['sb_flags'] & 0x0001:
            miscflags += " Signed_Directory_Hash "
        if self.ext4_superblock['sb_flags'] & 0x0002:
            miscflags += " Unsigned_Directory_Hash "
        if self.ext4_superblock['sb_flags'] & 0x0004:
            miscflags += " Test_File_System "
        if self.ext4_superblock['sb_flags'] & 0x0010:
            miscflags += " Snapshot_Enabled "
        if self.ext4_superblock['sb_flags'] & 0x0020:
            miscflags += " Snapshot_Fix "
        if self.ext4_superblock['sb_flags'] & 0x0040:
            miscflags += " Fix_Exclude "                    
        self.ext4_superblock['sb_raid_stride'] = int.from_bytes(self.f[offset+0x164:offset+0x166], byteorder='little')
        self.ext4_superblock['sb_mmp_interval'] = int.from_bytes(self.f[offset+0x166:offset+0x168], byteorder='little')
        self.ext4_superblock['sb_mmp_block'] = int.from_bytes(self.f[offset+0x168:offset+0x170], byteorder='little')
        self.ext4_superblock['sb_raid_stripe_width'] = int.from_bytes(self.f[offset+0x170:offset+0x174], byteorder='little')
        self.ext4_superblock['sb_log_groups_per_flex'] = int.from_bytes(self.f[offset+0x174:offset+0x175], byteorder='little')
        # print(f"Log Groups per Flex: {self.ext4_superblock['sb_log_groups_per_flex']}")
        self.ext4_superblock['sb_reserved_char_pad2'] = int.from_bytes(self.f[offset+0x175:offset+0x176], byteorder='little')
        self.ext4_superblock['sb_reserved_pad'] = self.f[offset+0x176:offset+0x178].hex()
        self.ext4_superblock['sb_kbytes_written'] = int.from_bytes(self.f[offset+0x178:offset+0x180], byteorder='little')
        self.ext4_superblock['sb_reserved'] = self.f[offset+0x180:offset+0x400].hex()
        print("\n\nEnd of Superblock Parsing\n\n")
            
    
    def parse_ext4_block_group_descriptor(self,offset): 
        self.ext4_blockgroupdescriptor['bg_block_bitmap_lo'] = int.from_bytes(self.f[offset+0x00:offset+0x04], byteorder='little')
        print(f"Block Bitmap: {self.ext4_blockgroupdescriptor['bg_block_bitmap_lo']}")
        self.ext4_blockgroupdescriptor['bg_inode_bitmap_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
        print(f"Inode Bitmap: {self.ext4_blockgroupdescriptor['bg_inode_bitmap_lo']}")
        self.ext4_blockgroupdescriptor['bg_inode_table_lo'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Inode Table: {self.ext4_blockgroupdescriptor['bg_inode_table_lo']}")
        self.ext4_blockgroupdescriptor['bg_free_blocks_count_lo'] = int.from_bytes(self.f[offset+0x0C:offset+0x0E], byteorder='little')
        print(f"Free Blocks: {self.ext4_blockgroupdescriptor['bg_free_blocks_count_lo']}")
        self.ext4_blockgroupdescriptor['bg_free_inodes_count_lo'] = int.from_bytes(self.f[offset+0x0E:offset+0x10], byteorder='little')
        print(f"Free Inodes: {self.ext4_blockgroupdescriptor['bg_free_inodes_count_lo']}")
        self.ext4_blockgroupdescriptor['bg_used_dirs_count_lo'] = int.from_bytes(self.f[offset+0x10:offset+0x12], byteorder='little')
        print(f"Used Directories: {self.ext4_blockgroupdescriptor['bg_used_dirs_count_lo']}")
        self.ext4_blockgroupdescriptor['bg_flags'] = int.from_bytes(self.f[offset+0x12:offset+0x14], byteorder='little')
        flags = ""
        if self.ext4_blockgroupdescriptor['bg_flags'] == 0:
            flags = "Inode Uninit"
        elif self.ext4_blockgroupdescriptor['bg_flags'] == 1:
            flags = "Block Uninit"
        print(f"Flags: {flags}")
        self.ext4_blockgroupdescriptor['bg_exclude_bitmap_lo'] = int.from_bytes(self.f[offset+0x14:offset+0x18], byteorder='little')
        print(f"Exclude Bitmap: {self.ext4_blockgroupdescriptor['bg_exclude_bitmap_lo']}")
        self.ext4_blockgroupdescriptor['bg_reserved1'] = int.from_bytes(self.f[offset+0x18:offset+0x1C], byteorder='little')
        print(f"Reserved1: {self.ext4_blockgroupdescriptor['bg_reserved1']}")
        self.ext4_blockgroupdescriptor['bg_itable_unused_lo'] = int.from_bytes(self.f[offset+0x1C:offset+0x1E], byteorder='little')
        print(f"Unused Inode Table: {self.ext4_blockgroupdescriptor['bg_itable_unused_lo']}")
        self.ext4_blockgroupdescriptor['bg_checksum'] = int.from_bytes(self.f[offset+0x1E:offset+0x20], byteorder='little')
        print(f"Checksum: {self.ext4_blockgroupdescriptor['bg_checksum']}")
        if self.ext4_superblock['sb_feature_incompat'] & EXT4_FEATURE_INCOMPAT['EXT4_FEATURE_INCOMPAT_64BIT'] and self.ext4_superblock['sb_desc_size'] > 32:
            print("\n\nFor EXT4_FEATURE_INCOMPAT_64BIT and 'sb_desc_size' > 32\n\n")
            self.ext4_blockgroupdescriptor['bg_block_bitmap_hi'] = int.from_bytes(self.f[offset+0x20:offset+0x24], byteorder='little')
            print(f"Block Bitmap Hi: {self.ext4_blockgroupdescriptor['bg_block_bitmap_hi']}")
            self.ext4_blockgroupdescriptor['bg_inode_bitmap_hi'] = int.from_bytes(self.f[offset+0x24:offset+0x28], byteorder='little')
            print(f"Inode Bitmap Hi: {self.ext4_blockgroupdescriptor['bg_inode_bitmap_hi']}")
            self.ext4_blockgroupdescriptor['bg_inode_table_hi'] = int.from_bytes(self.f[offset+0x28:offset+0x2C], byteorder='little')
            print(f"Inode Table Hi: {self.ext4_blockgroupdescriptor['bg_inode_table_hi']}")
            self.ext4_blockgroupdescriptor['bg_free_blocks_count_hi'] = int.from_bytes(self.f[offset+0x2C:offset+0x2E], byteorder='little')
            print(f"Free Blocks Hi: {self.ext4_blockgroupdescriptor['bg_free_blocks_count_hi']}")
            self.ext4_blockgroupdescriptor['bg_free_inodes_count_hi'] = int.from_bytes(self.f[offset+0x2E:offset+0x30], byteorder='little')
            print(f"Free Inodes Hi: {self.ext4_blockgroupdescriptor['bg_free_inodes_count_hi']}")
            self.ext4_blockgroupdescriptor['bg_used_dirs_count_hi'] = int.from_bytes(self.f[offset+0x30:offset+0x32], byteorder='little')
            print(f"Used Directories Hi: {self.ext4_blockgroupdescriptor['bg_used_dirs_count_hi']}")
            self.ext4_blockgroupdescriptor['bg_itable_unused_hi'] = int.from_bytes(self.f[offset+0x32:offset+0x34], byteorder='little')
            print(f"Unused Inode Table Hi: {self.ext4_blockgroupdescriptor['bg_itable_unused_hi']}")
            self.ext4_blockgroupdescriptor['bg_exclude_bitmap_hi'] = int.from_bytes(self.f[offset+0x34:offset+0x38], byteorder='little')
            print(f"Exclude Bitmap Hi: {self.ext4_blockgroupdescriptor['bg_exclude_bitmap_hi']}")
            self.ext4_blockgroupdescriptor['bg_reserved2'] = int.from_bytes(self.f[offset+0x38:offset+0x3C], byteorder='little')
            print(f"Reserved2: {self.ext4_blockgroupdescriptor['bg_reserved2']}")
            self.ext4_blockgroupdescriptor['bg_reserved3'] = int.from_bytes(self.f[offset+0x3C:offset+0x40], byteorder='little')
            print(f"Reserved3: {self.ext4_blockgroupdescriptor['bg_reserved3']}")
        
    def parse_ext4_inode_table(self,offset,group_num):
        inode_size = self.ext4_superblock['sb_inode_size']
        inode_count = self.ext4_superblock['sb_inodes_per_group']
        for i in range(inode_count):
            # print(f"\n\nParsing Inode {i}:\n\n")
            # if i==784898:
                # exit()
            # print(f"\n\nParsing Inode {(group_num*self.ext4_superblock['sb_inodes_per_group'])+i}:\n\n")
            # if (group_num*self.ext4_superblock['sb_inodes_per_group'])+i ==784897:
            #     exit()
            self.parse_ext4_inode(offset+(i*inode_size),i, group_num)
            inodeoffset=offset+(i*inode_size)
            if int.from_bytes(self.f[inodeoffset+0x04:inodeoffset+0x08], byteorder='little') == 0:
                continue
            if int.from_bytes(self.f[inodeoffset+0x02:inodeoffset+0x04], byteorder='little') == 0 and int.from_bytes(self.f[inodeoffset+0x28:inodeoffset+0x2C], byteorder='little') == 0:
                continue 
            print("\n-----Parsing Extended Attributes-----\n")
            self.ext4_parse_xattr((offset+(i*inode_size))+160)
            print("\n-----End of Extended Attributes-----\n")
            print("\n-----Parsing Extent Tree-----\n")
            self.parse_ext4_extenttree(offset+(i*inode_size)+0x28)
            print("\n-----End of Extent Tree-----\n")
            extoffset=offset+((i*inode_size)+0x28)
            # print(self.ext4_inode['i_flags'])
            if ((self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'])&1) == 1:
                self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                if self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==0:
                    ee_block=[]
                    save_extoffset=extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                            self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                            self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                            self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                            self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                            ee_block.append(self.ext4_extent['ee_block'])
                            extoffset=extoffset+12
                    log_offset=[]
                    log_number=[]
                    extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        ogloglen=len(log_number)
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        for i in range(len(log_number),ee_block[i]):
                            log_number.append(i)
                            log_offset.append(self.ext4_extent['ee_start_lo']*(i-ogloglen)*4096)
                        extoffset=extoffset+0x12
                    extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')    
                        self.ext4_parse_hashtree(self.ext4_extent['ee_start_lo'],log_number,log_offset)
                        extoffset=extoffset+0x18
                elif self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==1:
                    self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                    self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                    extoffset=extoffset+0x18
                    extoffset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                    self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                    self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                    self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                    self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                    self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                    ee_block=[]
                    save_extoffset=extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        ee_block.append(self.ext4_extent['ee_block'])
                        extoffset=extoffset+12
                        log_offset=[]
                        log_number=[]
                        extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        ogloglen=len(log_number)
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        for i in range(len(log_number),ee_block[i]):
                            log_number.append(i)
                            log_offset.append(self.ext4_extent['ee_start_lo']*(i-ogloglen)*4096)
                        extoffset=extoffset+0x12
                    extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')    
                        self.ext4_parse_hashtree(self.ext4_extent['ee_start_lo'],log_number,log_offset)
                        extoffset=extoffset+0x18
                elif self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==2:
                    self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                    self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                    extoffset=extoffset+0x18
                    extoffset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                    self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                    self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                    self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                    self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                    self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                    self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                    self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                    extoffset=extoffset+0x18
                    extoffset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                    self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                    self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                    self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                    self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                    self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                    ee_block=[]
                    save_extoffset=extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        ee_block.append(self.ext4_extent['ee_block'])
                        extoffset=extoffset+12
                        log_offset=[]
                        log_number=[]
                        extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        ogloglen=len(log_number)
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        for i in range(len(log_number),ee_block[i]):
                            log_number.append(i)
                            log_offset.append(self.ext4_extent['ee_start_lo']*(i-ogloglen)*4096)
                        extoffset=extoffset+0x12
                    extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')    
                        self.ext4_parse_hashtree(self.ext4_extent['ee_start_lo'],log_number,log_offset)
                        extoffset=extoffset+0x18
                elif self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==3:
                    self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                    self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                    extoffset=extoffset+0x18
                    extoffset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                    self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                    self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                    self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                    self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                    self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                    self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                    self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                    extoffset=extoffset+0x18
                    extoffset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                    self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                    self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                    self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                    self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                    self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                    self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                    self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                    self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                    extoffset=extoffset+0x18
                    extoffset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                    self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                    self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                    self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                    self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                    self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                    ee_block=[]
                    save_extoffset=extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        ee_block.append(self.ext4_extent['ee_block'])
                        extoffset=extoffset+12
                        log_offset=[]
                        log_number=[]
                        extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        ogloglen=len(log_number)
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')
                        for i in range(len(log_number),ee_block[i]):
                            log_number.append(i)
                            log_offset.append(self.ext4_extent['ee_start_lo']*(i-ogloglen)*4096)
                        extoffset=extoffset+0x12
                    extoffset=save_extoffset
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_extent['ee_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent['ee_len'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x12], byteorder='little')
                        self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[extoffset+0x12:extoffset+0x14], byteorder='little')
                        self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x18], byteorder='little')    
                        self.ext4_parse_hashtree(self.ext4_extent['ee_start_lo'],log_number,log_offset)
                        extoffset=extoffset+0x18
                    # print(f"Block: {self.ext4_extent['ee_block']} Length: {self.ext4_extent['ee_len']} Start: {self.ext4_extent['ee_start_hi']}:{self.ext4_extent['ee_start_lo']}")
            else:
                self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[extoffset+0x00:extoffset+0x02], byteorder='little')
                self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[extoffset+0x02:extoffset+0x04], byteorder='little')
                self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[extoffset+0x04:extoffset+0x06], byteorder='little')
                self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[extoffset+0x06:extoffset+0x08], byteorder='little')
                self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[extoffset+0x08:extoffset+0x0C], byteorder='little')
                # print("well")
                if self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==0:
                    # print("depth1")
                    for i in range(self.ext4_extent_header_copy['eh_entries']):
                        self.ext4_parse_direntry(extoffset+(0x0C*(i+1)))
                    # if self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'] != 0:
                    #     continue
                elif self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==1:
                    for ent in range(self.ext4_extent_header_copy['eh_entries']):
                        extoffset=extoffset+(0x0C*ent)
                        self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                        self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                        self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                        new_offset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                        self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[new_offset+0x00:new_offset+0x02], byteorder='little')
                        self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[new_offset+0x02:new_offset+0x04], byteorder='little')
                        self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[new_offset+0x04:new_offset+0x06], byteorder='little')
                        self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[new_offset+0x06:new_offset+0x08], byteorder='little')
                        self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[new_offset+0x08:new_offset+0x0C], byteorder='little')
                        new_offset1=new_offset+0x0C
                        for i in range(self.ext4_extent_header_copy['eh_entries']):
                            self.ext4_parse_direntry(new_offset1+(0x0C*i))
                    # if self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'] != 0:
                    #     continue
                elif self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==2:
                    for ent in range(self.ext4_extent_header_copy['eh_entries']):
                        extoffset=extoffset+(0x0C*ent)
                        self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                        self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                        self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                        new_offset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                        self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[new_offset+0x00:new_offset+0x02], byteorder='little')
                        self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[new_offset+0x02:new_offset+0x04], byteorder='little')
                        self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[new_offset+0x04:new_offset+0x06], byteorder='little')
                        self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[new_offset+0x06:new_offset+0x08], byteorder='little')
                        self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[new_offset+0x08:new_offset+0x0C], byteorder='little')
                        for ent1 in range(self.ext4_extent_header_copy['eh_entries']):
                            new_offset=new_offset+(0x0C*ent1)
                            self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[new_offset+0x0C:new_offset+0x10], byteorder='little')
                            self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[new_offset+0x10:new_offset+0x14], byteorder='little')
                            self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[new_offset+0x14:new_offset+0x16], byteorder='little')
                            self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[new_offset+0x16:new_offset+0x18], byteorder='little')
                            new_offset1=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                            self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[new_offset1+0x00:new_offset1+0x02], byteorder='little')
                            self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[new_offset1+0x02:new_offset1+0x04], byteorder='little')
                            self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[new_offset1+0x04:new_offset1+0x06], byteorder='little')
                            self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[new_offset1+0x06:new_offset1+0x08], byteorder='little')
                            self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[new_offset1+0x08:new_offset1+0x0C], byteorder='little')
                            new_offset2=new_offset1+0x0C
                            for ent2 in range(self.ext4_extent_header_copy['eh_entries']):
                                self.ext4_parse_direntry(new_offset2*ent2)
                            # if self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'] != 0:
                            #     continue
                elif self.ext4_extent_header_copy['eh_magic']==0xF30A and self.ext4_extent_header_copy['eh_depth']==3:
                    for ent in range(self.ext4_extent_header_copy['eh_entries']):
                        extoffset=extoffset+(0x0C*ent)
                        self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[extoffset+0x0C:extoffset+0x10], byteorder='little')
                        self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[extoffset+0x10:extoffset+0x14], byteorder='little')
                        self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[extoffset+0x14:extoffset+0x16], byteorder='little')
                        self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[extoffset+0x16:extoffset+0x18], byteorder='little')
                        new_offset=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                        self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[new_offset+0x00:new_offset+0x02], byteorder='little')
                        self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[new_offset+0x02:new_offset+0x04], byteorder='little')
                        self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[new_offset+0x04:new_offset+0x06], byteorder='little')
                        self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[new_offset+0x06:new_offset+0x08], byteorder='little')
                        self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[new_offset+0x08:new_offset+0x0C], byteorder='little')
                        for ent1 in range(self.ext4_extent_header_copy['eh_entries']):
                            new_offset=new_offset+(0x0C*ent1)
                            self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[new_offset+0x0C:new_offset+0x10], byteorder='little')
                            self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[new_offset+0x10:new_offset+0x14], byteorder='little')
                            self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[new_offset+0x14:new_offset+0x16], byteorder='little')
                            self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[new_offset+0x16:new_offset+0x18], byteorder='little')
                            new_offset1=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                            self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[new_offset1+0x00:new_offset1+0x02], byteorder='little')
                            self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[new_offset1+0x02:new_offset1+0x04], byteorder='little')
                            self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[new_offset1+0x04:new_offset1+0x06], byteorder='little')
                            self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[new_offset1+0x06:new_offset1+0x08], byteorder='little')
                            self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[new_offset1+0x08:new_offset1+0x0C], byteorder='little')
                            new_offset2=new_offset1+0x0C
                            for ent2 in range(self.ext4_extent_header_copy['eh_entries']):
                                new_offset2=new_offset2+(0x0C*ent2)
                                self.ext4_extent_idx_copy['ei_block'] = int.from_bytes(self.f[new_offset2+0x0C:new_offset2+0x10], byteorder='little')
                                self.ext4_extent_idx_copy['ei_leaf_lo'] = int.from_bytes(self.f[new_offset2+0x10:new_offset2+0x14], byteorder='little')
                                self.ext4_extent_idx_copy['ei_leaf_hi'] = int.from_bytes(self.f[new_offset2+0x14:new_offset2+0x16], byteorder='little')
                                self.ext4_extent_idx_copy['ei_unused'] = int.from_bytes(self.f[new_offset2+0x16:new_offset2+0x18], byteorder='little')
                                new_offset3=self.ext4_extent_idx_copy['ei_leaf_lo']*4096
                                self.ext4_extent_header_copy['eh_magic'] = int.from_bytes(self.f[new_offset3+0x00:new_offset3+0x02], byteorder='little')
                                self.ext4_extent_header_copy['eh_entries'] = int.from_bytes(self.f[new_offset3+0x02:new_offset3+0x04], byteorder='little')
                                self.ext4_extent_header_copy['eh_max'] = int.from_bytes(self.f[new_offset3+0x04:new_offset3+0x06], byteorder='little')
                                self.ext4_extent_header_copy['eh_depth'] = int.from_bytes(self.f[new_offset3+0x06:new_offset3+0x08], byteorder='little')
                                self.ext4_extent_header_copy['eh_generation'] = int.from_bytes(self.f[new_offset3+0x08:new_offset3+0x0C], byteorder='little')
                                new_offset3=new_offset3+0x0C
                                for ent3 in range(self.ext4_extent_header_copy['eh_entries']):
                                    self.ext4_parse_direntry(new_offset3*ent3)
                    # if self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'] != 0:
                    
                    #     continue
                                
                # self.ext4_parse_dir(offset+(i*inode_size))


    def ext4_parse_hashtree(self, offset, log_number, log_offset):
        offset=offset*4096
        self.dx_root['dot_inode']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
        print(f"Inode: {self.dx_root['dot_inode']}")
        self.dx_root['dot_rec_len']=int.from_bytes(self.f[offset+0x04:offset+0x06],byteorder='little')
        print(f"Record Length: {self.dx_root['dot_rec_len']}")
        rec_len=self.dx_root['dot_rec_len']
        self.dx_root['dot_name_len']=int.from_bytes(self.f[offset+0x06:offset+0x07],byteorder='little')
        print(f"Name Length: {self.dx_root['dot_name_len']}")
        self.dx_root['dot_file_type']=int.from_bytes(self.f[offset+0x07:offset+0x08],byteorder='little')
        print(f"File Type: {self.dx_root['dot_file_type']}")
        self.dx_root['dot_name']=self.f[offset+0x08:offset+0x0C].hex()
        print(f"Name: {self.dx_root['dot_name']}")
        self.dx_root['dot_dot_inode']=int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
        print(f"Inode: {self.dx_root['dot_dot_inode']}")
        self.dx_root['dot_dot_rec_len']=int.from_bytes(self.f[offset+0x10:offset+0x12],byteorder='little')
        print(f"Record Length: {self.dx_root['dot_dot_rec_len']}")
        rec_len=self.dx_root['dot_dot_rec_len']
        self.dx_root['dot_dot_name_len']=int.from_bytes(self.f[offset+0x12:offset+0x13],byteorder='little')
        print(f"Name Length: {self.dx_root['dot_dot_name_len']}")
        self.dx_root['dot_dot_file_type']=int.from_bytes(self.f[offset+0x13:offset+0x14],byteorder='little')
        print(f"File Type: {self.dx_root['dot_dot_file_type']}")
        self.dx_root['dot_dot_name']=self.f[offset+0x14:offset+0x18].hex()
        print(f"Name: {self.dx_root['dot_dot_name']}")
        self.dx_root['reserved_zero']=int.from_bytes(self.f[offset+0x18:offset+0x1C], byteorder='little')
        print(f"Reserved Zero: {self.dx_root['reserved_zero']}")
        self.dx_root['hash_version']=int.from_bytes(self.f[offset+0x1C:offset+0x1D], byteorder='little')
        # print(f"Hash Version: {self.dx_root['hash_version']}")
        hash_version=""
        if self.dx_root['hash_version'] == 0:
            hash_version="Legacy"
        elif self.dx_root['hash_version'] == 1:
            hash_version="Half MD4"
        elif self.dx_root['hash_version'] == 2:
            hash_version="Tea"
        elif self.dx_root['hash_version'] == 3:
            hash_version="Legacy Unsigned"
        elif self.dx_root['hash_version'] == 4:
            hash_version="Unsigned,Half MD4"
        elif self.dx_root['hash_version'] == 5:
            hash_version="Unsigned,Tea"
        elif self.dx_root['hash_version'] == 6:
            hash_version="Splash"
        print(f"Hash Version: {hash_version}")
        self.dx_root['info_length']=int.from_bytes(self.f[offset+0x1D:offset+0x1E], byteorder='little')
        print(f"Info Length: {self.dx_root['info_length']}")  
        self.dx_root['indirect_levels']=int.from_bytes(self.f[offset+0x1E:offset+0x1F], byteorder='little')
        print(f"Indirect Levels: {self.dx_root['indirect_levels']}")
        self.dx_root['unused_flags']=int.from_bytes(self.f[offset+0x1F:offset+0x20], byteorder='little')
        print(f"Unused Flags: {self.dx_root['unused_flags']}")
        self.dx_root['limit']=int.from_bytes(self.f[offset+0x20:offset+0x22], byteorder='little')
        print(f"Limit: {self.dx_root['limit']}")
        self.dx_root['count']=int.from_bytes(self.f[offset+0x22:offset+0x24], byteorder='little')
        print(f"Count: {self.dx_root['count']}")
        self.dx_root['block']=int.from_bytes(self.f[offset+0x24:offset+0x28], byteorder='little')
        print(f"Block: {self.dx_root['block']}")        
        offset=offset+0x28
        valid_ent=self.dx_root['count']
        indirectlevel=self.dx_root['indirect_levels']
        if self.dx_root['indirect_levels']==0:
            for i in range(0, valid_ent, 1):
                print(f"Entry: {i}")
                self.dx_entry['hash']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                print(f"Hash: {self.dx_entry['hash']}")
                self.dx_entry['block']=int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                print(f"Block: {self.dx_entry['block']}")
                diroff=0
                for i in range(len(log_number)):
                    if log_number[i]==self.dx_root['block']:
                        diroff=log_offset[i]
                        break
                offset=offset+0x08
                self.ext4_parse_linear_dir_entry_info(diroff)
        elif self.dx_root['indirect_levels']==1:
            for i in range(0, valid_ent, 1):
                print(f"Entry: {i}")
                self.dx_entry['hash']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                print(f"Hash: {self.dx_entry['hash']}")
                self.dx_entry['block']=int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                print(f"Block: {self.dx_entry['block']}")
                diroff=0
                for i in range(len(log_number)):
                    if log_number[i]==self.dx_root['block']:
                        diroff=log_offset[i]
                        self.print_ext4_htree(diroff)
                        diroff=diroff+0x08
                        for i in range(0, self.dx_root['count'], 1):
                            
                            self.dx_entry['hash']=int.from_bytes(self.f[diroff:diroff+0x04], byteorder='little')
                            print(f"Hash: {self.dx_entry['hash']}")
                            self.dx_entry['block']=int.from_bytes(self.f[diroff+0x04:diroff+0x08], byteorder='little')
                            print(f"Block: {self.dx_entry['block']}")
                            dir2=0
                            for i in range(len(log_number)):
                                if log_number[i]==self.dx_entry['block']:
                                    dir2=log_offset[i]
                                    break
                            self.ext4_parse_linear_dir_entry_info(dir2)
                            diroff=diroff+0x08
                offset=offset+0x08
        elif self.dx_root['indirect_levels']==2:
            for i in range(0, valid_ent, 1):
                print(f"Entry: {i}")
                self.dx_entry['hash']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                print(f"Hash: {self.dx_entry['hash']}")
                self.dx_entry['block']=int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                print(f"Block: {self.dx_entry['block']}")
                diroff=0
                for i in range(len(log_number)):
                    if log_number[i]==self.dx_root['block']:
                        diroff=log_offset[i]
                        self.print_ext4_htree(diroff)
                        diroff=diroff+0x08
                        for i in range(0, self.dx_root['count'], 1):
                            self.dx_entry['hash']=int.from_bytes(self.f[diroff:diroff+0x04], byteorder='little')
                            print(f"Hash: {self.dx_entry['hash']}")
                            self.dx_entry['block']=int.from_bytes(self.f[diroff+0x04:diroff+0x08], byteorder='little')
                            print(f"Block: {self.dx_entry['block']}")
                            diroff2=0
                            for i in range(len(log_number)):
                                if log_number[i]==self.dx_entry['block']:
                                    diroff2=log_offset[i]
                                    self.print_ext4_htree(diroff2)
                                    diroff2=diroff2+0x08
                                    for i in range(0, self.dx_root['count'], 1):
                                        self.dx_entry['hash']=int.from_bytes(self.f[diroff2:diroff2+0x04], byteorder='little')
                                        print(f"Hash: {self.dx_entry['hash']}")
                                        self.dx_entry['block']=int.from_bytes(self.f[diroff2+0x04:diroff2+0x08], byteorder='little')
                                        print(f"Block: {self.dx_entry['block']}")
                                        dir3=0
                                        for i in range(len(log_number)):
                                            if log_number[i]==self.dx_entry['block']:
                                                dir3=log_offset[i]
                                                break
                                        self.ext4_parse_linear_dir_entry_info(dir3)
                                        diroff2=diroff2+0x08
                            diroff=diroff+0x08
                offset=offset+0x08
        elif self.dx_root['indirect_levels']==3:
            for i in range(0, valid_ent, 1):
                print(f"Entry: {i}")
                self.dx_entry['hash']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                print(f"Hash: {self.dx_entry['hash']}")
                self.dx_entry['block']=int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                print(f"Block: {self.dx_entry['block']}")
                diroff=0
                for i in range(len(log_number)):
                    if log_number[i]==self.dx_root['block']:
                        diroff=log_offset[i]
                        self.print_ext4_htree(diroff)
                        diroff=diroff+0x08
                        for i in range(0, self.dx_root['count'], 1):
                            self.dx_entry['hash']=int.from_bytes(self.f[diroff:diroff+0x04], byteorder='little')
                            print(f"Hash: {self.dx_entry['hash']}")
                            self.dx_entry['block']=int.from_bytes(self.f[diroff+0x04:diroff+0x08], byteorder='little')
                            print(f"Block: {self.dx_entry['block']}")
                            diroff2=0
                            for i in range(len(log_number)):
                                if log_number[i]==self.dx_entry['block']:
                                    diroff2=log_offset[i]
                                    self.print_ext4_htree(diroff2)
                                    diroff2=diroff2+0x08
                                    for i in range(0, self.dx_root['count'], 1):
                                        self.dx_entry['hash']=int.from_bytes(self.f[diroff2:diroff2+0x04], byteorder='little')
                                        print(f"Hash: {self.dx_entry['hash']}")
                                        self.dx_entry['block']=int.from_bytes(self.f[diroff2+0x04:diroff2+0x08], byteorder='little')
                                        print(f"Block: {self.dx_entry['block']}")
                                        diroff3=0
                                        for i in range(len(log_number)):
                                            if log_number[i]==self.dx_entry['block']:
                                                diroff3=log_offset[i]
                                                self.print_ext4_htree(diroff3)
                                                diroff3=diroff3+0x08
                                                for i in range(0, self.dx_root['count'], 1):
                                                    self.dx_entry['hash']=int.from_bytes(self.f[diroff3:diroff3+0x04], byteorder='little')
                                                    print(f"Hash: {self.dx_entry['hash']}")
                                                    self.dx_entry['block']=int.from_bytes(self.f[diroff3+0x04:diroff3+0x08], byteorder='little')
                                                    print(f"Block: {self.dx_entry['block']}")
                                                    dir4=0
                                                    for i in range(len(log_number)):
                                                        if log_number[i]==self.dx_entry['block']:
                                                            dir4=log_offset[i]
                                                            break
                                                    self.ext4_parse_linear_dir_entry_info(dir4)
                                                    diroff3=diroff3+0x08
                                        diroff2=diroff2+0x08
                            diroff=diroff+0x08
                offset=offset+0x08

    
    def print_ext4_htree(self,offset):
        self.dx_root['dot_inode']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
        print(f"Inode: {self.dx_root['dot_inode']}")
        self.dx_root['dot_rec_len']=int.from_bytes(self.f[offset+0x04:offset+0x06],byteorder='little')
        print(f"Record Length: {self.dx_root['dot_rec_len']}")
        rec_len=self.dx_root['dot_rec_len']
        self.dx_root['dot_name_len']=int.from_bytes(self.f[offset+0x06:offset+0x07],byteorder='little')
        print(f"Name Length: {self.dx_root['dot_name_len']}")
        self.dx_root['dot_file_type']=int.from_bytes(self.f[offset+0x07:offset+0x08],byteorder='little')
        print(f"File Type: {self.dx_root['dot_file_type']}")
        self.dx_root['dot_name']=self.f[offset+0x08:offset+0x0C].hex()
        print(f"Name: {self.dx_root['dot_name']}")
        self.dx_root['dot_dot_inode']=int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
        print(f"Inode: {self.dx_root['dot_dot_inode']}")
        self.dx_root['dot_dot_rec_len']=int.from_bytes(self.f[offset+0x10:offset+0x12],byteorder='little')
        print(f"Record Length: {self.dx_root['dot_dot_rec_len']}")
        rec_len=self.dx_root['dot_dot_rec_len']
        self.dx_root['dot_dot_name_len']=int.from_bytes(self.f[offset+0x12:offset+0x13],byteorder='little')
        print(f"Name Length: {self.dx_root['dot_dot_name_len']}")
        self.dx_root['dot_dot_file_type']=int.from_bytes(self.f[offset+0x13:offset+0x14],byteorder='little')
        print(f"File Type: {self.dx_root['dot_dot_file_type']}")
        self.dx_root['dot_dot_name']=self.f[offset+0x14:offset+0x18].hex()
        print(f"Name: {self.dx_root['dot_dot_name']}")
        self.dx_root['reserved_zero']=int.from_bytes(self.f[offset+0x18:offset+0x1C], byteorder='little')
        print(f"Reserved Zero: {self.dx_root['reserved_zero']}")
        self.dx_root['hash_version']=int.from_bytes(self.f[offset+0x1C:offset+0x1D], byteorder='little')
        # print(f"Hash Version: {self.dx_root['hash_version']}")
        hash_version=""
        if self.dx_root['hash_version'] == 0:
            hash_version="Legacy"
        elif self.dx_root['hash_version'] == 1:
            hash_version="Half MD4"
        elif self.dx_root['hash_version'] == 2:
            hash_version="Tea"
        elif self.dx_root['hash_version'] == 3:
            hash_version="Legacy Unsigned"
        elif self.dx_root['hash_version'] == 4:
            hash_version="Unsigned,Half MD4"
        elif self.dx_root['hash_version'] == 5:
            hash_version="Unsigned,Tea"
        elif self.dx_root['hash_version'] == 6:
            hash_version="Splash"
        print(f"Hash Version: {hash_version}")
        self.dx_root['info_length']=int.from_bytes(self.f[offset+0x1D:offset+0x1E], byteorder='little')
        print(f"Info Length: {self.dx_root['info_length']}")  
        self.dx_root['indirect_levels']=int.from_bytes(self.f[offset+0x1E:offset+0x1F], byteorder='little')
        print(f"Indirect Levels: {self.dx_root['indirect_levels']}")
        self.dx_root['unused_flags']=int.from_bytes(self.f[offset+0x1F:offset+0x20], byteorder='little')
        print(f"Unused Flags: {self.dx_root['unused_flags']}")
        self.dx_root['limit']=int.from_bytes(self.f[offset+0x20:offset+0x22], byteorder='little')
        print(f"Limit: {self.dx_root['limit']}")
        self.dx_root['count']=int.from_bytes(self.f[offset+0x22:offset+0x24], byteorder='little')
        print(f"Count: {self.dx_root['count']}")
        self.dx_root['block']=int.from_bytes(self.f[offset+0x24:offset+0x28], byteorder='little')
        print(f"Block: {self.dx_root['block']}")  

    def parse_ext4_inode(self,offset,inode_num,group_num):
        if self.DEBUG==False and int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little') == 0:
            return 
        if int.from_bytes(self.f[offset+0x02:offset+0x04],byteorder = 'little')==0 and int.from_bytes(self.f[offset+0x28:offset+0x2C],byteorder='little')==0:
            return
        print(f"\n\nParsing Inode {(group_num*self.ext4_superblock['sb_inodes_per_group'])+inode_num+1}:\n\n")
        idchk=((group_num*self.ext4_superblock['sb_inodes_per_group'])+inode_num+1)
        # print(hex(offset))
        # if idchk == 525749:
        #     exit()
        # print(inode_num)
        # print(group_num)
        # print(self.ext4_superblock['sb_inodes_per_group'])
        self.ext4_inode['i_mode'] = int.from_bytes(self.f[offset+0x00:offset+0x02], byteorder='little')
        print(f"Mode: {self.ext4_inode['i_mode']}")
        self.ext4_inode['i_uid'] = int.from_bytes(self.f[offset+0x02:offset+0x04], byteorder='little')
        print(f"UID: {self.ext4_inode['i_uid']}")
        self.ext4_inode['i_size_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
        print(f"Size: {self.ext4_inode['i_size_lo']}")
        self.ext4_inode['i_atime'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Access Time: {datetime.utcfromtimestamp(self.ext4_inode['i_atime']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_inode['i_ctime'] = int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
        print(f"Creation Time: {datetime.utcfromtimestamp(self.ext4_inode['i_ctime']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_inode['i_mtime'] = int.from_bytes(self.f[offset+0x10:offset+0x14], byteorder='little')
        print(f"Modification Time: {datetime.utcfromtimestamp(self.ext4_inode['i_mtime']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_inode['i_dtime'] = int.from_bytes(self.f[offset+0x14:offset+0x18], byteorder='little')
        print(f"Deletion Time: {datetime.utcfromtimestamp(self.ext4_inode['i_dtime']).strftime('%Y-%m-%d %H:%M:%S')}")
        self.ext4_inode['i_gid'] = int.from_bytes(self.f[offset+0x18:offset+0x1A], byteorder='little')
        print(f"GID: {self.ext4_inode['i_gid']}")
        self.ext4_inode['i_links_count'] = int.from_bytes(self.f[offset+0x1A:offset+0x1C], byteorder='little')
        print(f"Links Count: {self.ext4_inode['i_links_count']}")
        self.ext4_inode['i_blocks_lo'] = int.from_bytes(self.f[offset+0x1C:offset+0x20], byteorder='little')
        print(f"Blocks: {self.ext4_inode['i_blocks_lo']}")
        self.ext4_inode['i_flags'] = int.from_bytes(self.f[offset+0x20:offset+0x24], byteorder='little')
        print(f"Flags: {self.ext4_inode['i_flags']}")
        self.ext4_inode['i_osd1'] = self.f[offset+0x24:offset+0x28].hex()
        print(f"OSD1: {self.ext4_inode['i_osd1']}")
        self.ext4_inode['i_block'] = []
        for i in range(15):
            self.ext4_inode['i_block'].append(int.from_bytes(self.f[offset+0x28+(i*4):offset+0x2C+(i*4)], byteorder='little'))
        print(f"Blocks: {self.ext4_inode['i_block']}")
        self.ext4_inode['i_generation'] = int.from_bytes(self.f[offset+0x64:offset+0x68], byteorder='little')
        print(f"Generation: {self.ext4_inode['i_generation']}")
        self.ext4_inode['i_file_acl_lo'] = int.from_bytes(self.f[offset+0x68:offset+0x6C], byteorder='little')
        print(f"File ACL: {self.ext4_inode['i_file_acl_lo']}")
        self.ext4_inode['i_size_high'] = int.from_bytes(self.f[offset+0x6C:offset+0x70], byteorder='little')
        print(f"Size High: {self.ext4_inode['i_size_high']}")
        self.ext4_inode['i_obso_faddr'] = int.from_bytes(self.f[offset+0x70:offset+0x74], byteorder='little')
        print(f"Obsolete Fragment Address: {self.ext4_inode['i_obso_faddr']}")
        self.ext4_inode['l_i_blocks_high'] = int.from_bytes(self.f[offset+0x74:offset+0x78], byteorder='little')
        print(f"Blocks High: {self.ext4_inode['l_i_blocks_high']}")
        self.ext4_inode['l_i_file_acl_high'] = int.from_bytes(self.f[offset+0x78:offset+0x7C], byteorder='little')
        print(f"File ACL High: {self.ext4_inode['l_i_file_acl_high']}")
        self.ext4_inode['l_i_uid_high'] = int.from_bytes(self.f[offset+0x7C:offset+0x80], byteorder='little')
        print(f"UID High: {self.ext4_inode['l_i_uid_high']}")
        self.ext4_inode['l_i_gid_high'] = int.from_bytes(self.f[offset+0x80:offset+0x84], byteorder='little')
        print(f"GID High: {self.ext4_inode['l_i_gid_high']}")
        self.ext4_inode['l_i_checksum_lo'] = int.from_bytes(self.f[offset+0x84:offset+0x88], byteorder='little')
        print(f"Checksum: {self.ext4_inode['l_i_checksum_lo']}")
        self.ext4_inode['l_i_reserved'] = int.from_bytes(self.f[offset+0x88:offset+0x90], byteorder='little')
        print(f"Reserved: {self.ext4_inode['l_i_reserved']}")
        self.ext4_inode['l_i_checksum_hi'] = int.from_bytes(self.f[offset+0x90:offset+0x94], byteorder='little')
        print(f"Checksum High: {self.ext4_inode['l_i_checksum_hi']}")
        self.ext4_inode['l_i_extra_isize'] = int.from_bytes(self.f[offset+0x94:offset+0x96], byteorder='little')
        print(f"Extra ISize: {self.ext4_inode['l_i_extra_isize']}")
        self.ext4_inode['l_i_ctime_extra'] = int.from_bytes(self.f[offset+0x96:offset+0x98], byteorder='little')
        print(f"CTime Extra: {self.ext4_inode['l_i_ctime_extra']}")
        self.ext4_inode['l_i_mtime_extra'] = int.from_bytes(self.f[offset+0x98:offset+0x9A], byteorder='little')
        print(f"MTime Extra: {self.ext4_inode['l_i_mtime_extra']}")
        self.ext4_inode['l_i_atime_extra'] = int.from_bytes(self.f[offset+0x9A:offset+0x9C], byteorder='little')
        print(f"ATime Extra: {self.ext4_inode['l_i_atime_extra']}")
        self.ext4_inode['l_i_crtime'] = int.from_bytes(self.f[offset+0x9C:offset+0xA0], byteorder='little')
        print(f"CRTime: {self.ext4_inode['l_i_crtime']}")
        self.ext4_inode['l_i_crtime_extra'] = int.from_bytes(self.f[offset+0xA0:offset+0xA2], byteorder='little')
        print(f"CRTime Extra: {self.ext4_inode['l_i_crtime_extra']}")
        self.ext4_inode['l_i_version_hi'] = int.from_bytes(self.f[offset+0xA2:offset+0xA4], byteorder='little')
        print(f"Version High: {self.ext4_inode['l_i_version_hi']}")
        self.ext4_inode['l_i_projid'] = int.from_bytes(self.f[offset+0xA4:offset+0xA6], byteorder='little')
        print(f"Project ID: {self.ext4_inode['l_i_projid']}")
        self.ext4_inode['l_i_reserved2'] = int.from_bytes(self.f[offset+0xA6:offset+0x100], byteorder='little')
        print("\n")
        
    def parse_ext4_extenttree(self,offset):
        self.ext4_extent_header['eh_magic'] = int.from_bytes(self.f[offset+0x00:offset+0x02], byteorder='little')
        print(f"Magic: {self.ext4_extent_header['eh_magic']}")
        self.ext4_extent_header['eh_entries'] = int.from_bytes(self.f[offset+0x02:offset+0x04], byteorder='little')
        print(f"Entries: {self.ext4_extent_header['eh_entries']}")
        self.ext4_extent_header['eh_max'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
        print(f"Max: {self.ext4_extent_header['eh_max']}")
        self.ext4_extent_header['eh_depth'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
        print(f"Depth: {self.ext4_extent_header['eh_depth']}")
        self.ext4_extent_header['eh_generation'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Generation: {self.ext4_extent_header['eh_generation']}")
        offset=offset+0x0C
        for i in range(0, self.ext4_extent_header['eh_entries'], 1):
            if self.ext4_extent_header['eh_depth'] == 0:
                self.ext4_extent['ee_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                self.ext4_extent['ee_len'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
                self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
                self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
                print("\n-----Parsing ext4 extent-----\n")
                print(f"Block: {self.ext4_extent['ee_block']}")
                print(f"Length: {self.ext4_extent['ee_len']}")
                print(f"Start Hi: {self.ext4_extent['ee_start_hi']}")
                print(f"Start Lo: {self.ext4_extent['ee_start_lo']}")
                offset=offset+0x0C
            elif self.ext4_extent_header['eh_depth'] == 1:
                self.ext4_extent_idx['ei_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                self.ext4_extent_idx['ei_leaf_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                self.ext4_extent_idx['ei_leaf_hi'] = int.from_bytes(self.f[offset+0x08:offset+0x0A], byteorder='little')
                self.ext4_extent_idx['ei_unused'] = int.from_bytes(self.f[offset+0x0A:offset+0x0C], byteorder='little')
                print("\n-----Parsing 1D ext4 extent index-----\n")
                print(f"Block: {self.ext4_extent_idx['ei_block']}")
                print(f"Leaf Lo: {self.ext4_extent_idx['ei_leaf_lo']}")
                print(f"Leaf Hi: {self.ext4_extent_idx['ei_leaf_hi']}")
                print(f"Unused: {self.ext4_extent_idx['ei_unused']}")
                offset=offset+0x0C
                self.ext4_parse_extenttree_idx1_pointer(self.ext4_extent_idx['ei_leaf_lo']*4096)
            elif self.ext4_extent_header['eh_depth'] == 2:
                self.ext4_extent_idx['ei_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                self.ext4_extent_idx['ei_leaf_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                self.ext4_extent_idx['ei_leaf_hi'] = int.from_bytes(self.f[offset+0x08:offset+0x0A], byteorder='little')
                self.ext4_extent_idx['ei_unused'] = int.from_bytes(self.f[offset+0x0A:offset+0x0C], byteorder='little')
                print("\n-----Parsing 2D ext4 extent index-----\n")
                print(f"Block: {self.ext4_extent_idx['ei_block']}")
                print(f"Leaf Lo: {self.ext4_extent_idx['ei_leaf_lo']}")
                print(f"Leaf Hi: {self.ext4_extent_idx['ei_leaf_hi']}")
                print(f"Unused: {self.ext4_extent_idx['ei_unused']}")
                offset=offset+0x0C
                self.ext4_parse_extenttree_idx2_pointer(self.ext4_extent_idx['ei_leaf_lo']*4096)
            elif self.ext4_extent_header['eh_depth'] == 3:
                self.ext4_extent_idx['ei_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
                self.ext4_extent_idx['ei_leaf_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
                self.ext4_extent_idx['ei_leaf_hi'] = int.from_bytes(self.f[offset+0x08:offset+0x0A], byteorder='little')
                self.ext4_extent_idx['ei_unused'] = int.from_bytes(self.f[offset+0x0A:offset+0x0C], byteorder='little')
                print("\n-----Parsing 3D ext4 extent index-----\n")
                print(f"Block: {self.ext4_extent_idx['ei_block']}")
                print(f"Leaf Lo: {self.ext4_extent_idx['ei_leaf_lo']}")
                print(f"Leaf Hi: {self.ext4_extent_idx['ei_leaf_hi']}")
                print(f"Unused: {self.ext4_extent_idx['ei_unused']}")
                offset=offset+0x0C
                self.ext4_parse_extenttree_idx3_pointer(self.ext4_extent_idx['ei_leaf_lo']*4096)    
                
                
                
    def ext4_parse_extenttree_idx1_pointer(self,offset):
        self.ext4_extent_header['eh_magic'] = int.from_bytes(self.f[offset+0x00:offset+0x02], byteorder='little')
        print(f"Magic: {self.ext4_extent_header['eh_magic']}")
        self.ext4_extent_header['eh_entries'] = int.from_bytes(self.f[offset+0x02:offset+0x04], byteorder='little')
        print(f"Entries: {self.ext4_extent_header['eh_entries']}")
        self.ext4_extent_header['eh_max'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
        print(f"Max: {self.ext4_extent_header['eh_max']}")
        self.ext4_extent_header['eh_depth'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
        print(f"Depth: {self.ext4_extent_header['eh_depth']}")
        self.ext4_extent_header['eh_generation'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Generation: {self.ext4_extent_header['eh_generation']}")
        offset=offset+0x0C
        for i in range(0, self.ext4_extent_header['eh_entries'], 1):
            self.ext4_extent['ee_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
            self.ext4_extent['ee_len'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
            self.ext4_extent['ee_start_hi'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
            self.ext4_extent['ee_start_lo'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
            print("\n-----Parsing 1D ext4 extent-----\n")
            print(f"Block: {self.ext4_extent['ee_block']}")
            print(f"Length: {self.ext4_extent['ee_len']}")
            print(f"Start Hi: {self.ext4_extent['ee_start_hi']}")
            print(f"Start Lo: {self.ext4_extent['ee_start_lo']}")
            offset=offset+0x0C
    
    def ext4_parse_extenttree_idx2_pointer(self,offset):
        self.ext4_extent_header['eh_magic'] = int.from_bytes(self.f[offset+0x00:offset+0x02], byteorder='little')
        print(f"Magic: {self.ext4_extent_header['eh_magic']}")
        self.ext4_extent_header['eh_entries'] = int.from_bytes(self.f[offset+0x02:offset+0x04], byteorder='little')
        print(f"Entries: {self.ext4_extent_header['eh_entries']}")
        self.ext4_extent_header['eh_max'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
        print(f"Max: {self.ext4_extent_header['eh_max']}")
        self.ext4_extent_header['eh_depth'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
        print(f"Depth: {self.ext4_extent_header['eh_depth']}")
        self.ext4_extent_header['eh_generation'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Generation: {self.ext4_extent_header['eh_generation']}")
        offset=offset+0x0C
        for i in range(0, self.ext4_extent_header['eh_entries'], 1):
            self.ext4_extent_idx['ei_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
            self.ext4_extent_idx['ei_leaf_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
            self.ext4_extent_idx['ei_leaf_hi'] = int.from_bytes(self.f[offset+0x08:offset+0x0A], byteorder='little')
            self.ext4_extent_idx['ei_unused'] = int.from_bytes(self.f[offset+0x0A:offset+0x0C], byteorder='little')
            print("\n-----Parsing 2D ext4 extent index-----\n")
            print(f"Block: {self.ext4_extent_idx['ei_block']}")
            print(f"Leaf Lo: {self.ext4_extent_idx['ei_leaf_lo']}")
            print(f"Leaf Hi: {self.ext4_extent_idx['ei_leaf_hi']}")
            print(f"Unused: {self.ext4_extent_idx['ei_unused']}")
            offset=offset+0x0C
            self.ext4_parse_extenttree_idx1_pointer(self.ext4_extent_idx['ei_leaf_lo']*4096)
        
    def ext4_parse_extenttree_idx3_pointer(self,offset):
        self.ext4_extent_header['eh_magic'] = int.from_bytes(self.f[offset+0x00:offset+0x02], byteorder='little')
        print(f"Magic: {self.ext4_extent_header['eh_magic']}")
        self.ext4_extent_header['eh_entries'] = int.from_bytes(self.f[offset+0x02:offset+0x04], byteorder='little')
        print(f"Entries: {self.ext4_extent_header['eh_entries']}")
        self.ext4_extent_header['eh_max'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
        print(f"Max: {self.ext4_extent_header['eh_max']}")
        self.ext4_extent_header['eh_depth'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
        print(f"Depth: {self.ext4_extent_header['eh_depth']}")
        self.ext4_extent_header['eh_generation'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Generation: {self.ext4_extent_header['eh_generation']}")
        offset=offset+0x0C
        for i in range(0, self.ext4_extent_header['eh_entries'], 1):
            self.ext4_extent_idx['ei_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
            self.ext4_extent_idx['ei_leaf_lo'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
            self.ext4_extent_idx['ei_leaf_hi'] = int.from_bytes(self.f[offset+0x08:offset+0x0A], byteorder='little')
            self.ext4_extent_idx['ei_unused'] = int.from_bytes(self.f[offset+0x0A:offset+0x0C], byteorder='little')
            print("\n-----Parsing 3D ext4 extent index-----\n")
            print(f"Block: {self.ext4_extent_idx['ei_block']}")
            print(f"Leaf Lo: {self.ext4_extent_idx['ei_leaf_lo']}")
            print(f"Leaf Hi: {self.ext4_extent_idx['ei_leaf_hi']}")
            print(f"Unused: {self.ext4_extent_idx['ei_unused']}")
            offset=offset+0x0C
            self.ext4_parse_extenttree_idx2_pointer(self.ext4_extent_idx['ei_leaf_lo']*4096)        
        
    def ext4_parse_xattr(self,offset):
        self.ext4_xattr_header['xh_magic'] = int.from_bytes(self.f[offset+0x00:offset+0x04], byteorder='little')
        print(f"Magic: {self.ext4_xattr_header['xh_magic']}")
        self.ext4_xattr_header['xh_refcount'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
        print(f"Refcount: {self.ext4_xattr_header['xh_refcount']}")
        self.ext4_xattr_header['xh_blocks'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Blocks: {self.ext4_xattr_header['xh_blocks']}")
        self.ext4_xattr_header['xh_hash'] = int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
        print(f"Hash: {self.ext4_xattr_header['xh_hash']}")
        self.ext4_xattr_header['xh_reserved'] = []
        for i in range(4):
            self.ext4_xattr_header['xh_reserved'].append(int.from_bytes(self.f[offset+0x10+(i*4):offset+0x14+(i*4)], byteorder='little'))
        print(f"Reserved: {self.ext4_xattr_header['xh_reserved']}")
        offset=offset+0x20
        offset=offset+16
        self.ext4_xattr_entry['xe_name_entry'] = int.from_bytes(self.f[offset:offset+0x01], byteorder='little')
        print(f"Name Entry: {self.ext4_xattr_entry['xe_name_entry']}")
        self.ext4_xattr_entry['xe_name_index'] = int.from_bytes(self.f[offset+0x01:offset+0x02], byteorder='little')
        print(f"Name Index: {self.ext4_xattr_entry['xe_name_index']}")
        self.ext4_xattr_entry['xe_value_offs'] = int.from_bytes(self.f[offset+0x02:offset+0x04], byteorder='little')
        print(f"Value Offset: {self.ext4_xattr_entry['xe_value_offs']}")
        self.ext4_xattr_entry['xe_value_block'] = int.from_bytes(self.f[offset+0x04:offset+0x08], byteorder='little')
        print(f"Value Block: {self.ext4_xattr_entry['xe_value_block']}")
        self.ext4_xattr_entry['xe_value_size'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        print(f"Value Size: {self.ext4_xattr_entry['xe_value_size']}")
        self.ext4_xattr_entry['xe_hash'] = int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
        print(f"Hash: {self.ext4_xattr_entry['xe_hash']}")
        self.ext4_xattr_entry['xe_name'] = int.from_bytes(self.f[offset+0x10:offset+0x30], byteorder='little')
        try:
            name = self.f[offset+0x10:offset+0x30].decode('utf-8')
            print(f"Name: {name}")
        except:
            name = self.f[offset+0x10:offset+0x30].hex()
            print(f"Name: {name}")
    
    #old parser code       
    # def ext4_parse_direntry(self,inodeoffset):
    #     # print("Reached")
    #     offset=inodeoffset
    #     self.ext4_extent_copy['ee_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
    #     self.ext4_extent_copy['ee_len'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
    #     self.ext4_extent_copy['ee_start_hi'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
    #     self.ext4_extent_copy['ee_start_lo'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
    #     print(self.ext4_extent_copy['ee_len'])
    #     offset=self.ext4_extent_copy['ee_start_lo']*4096
    #     dir_sz = self.ext4_extent_copy['ee_len'] * 4096
    #     print("\ndirectory size is",dir_sz,"\n")
    #     if dir_sz==0: 
    #         return
    #     i=0
    #     while i < dir_sz:
    #         dirent_sz=self.ext4_parse_direntry_internal(offset)
    #         if self.ext4_dir_entry_2['inode'] == 0 and self.ext4_dir_entry_2['rec_len'] > 263:
    #             offset=offset+4
    #             continue
    #         if self.ext4_dir_entry_2['name_len'] == 0 and self.ext4_dir_entry_2['inode'] != 0:
    #             offset=offset+0x08
    #             continue
    #         if self.ext4_dir_entry_2['rec_len'] > 263 and self.ext4_dir_entry_2['name']!="..":
    #             offset=offset+0x08
    #             continue
    #         if dirent_sz==0:
    #             break
                
    #         if(self.ext4_inode['i_mode'] & 0xF000) == 0x4000:
    #             if (self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'] )&1 == 1:
    #                 if self.dx_root['dot_inode'] != 0:
    #                     pass
    #                     # print("---------------------hashtree---------------------------")
    #                     # exit()
    #             else:
    #                 if self.ext4_dir_entry_2['inode'] != 0:
    #                     self.ext4_parse_linear_dir_entry_info(offset)
    #                     offset=offset+dirent_sz
    #         i=i+dirent_sz
     
    def ext4_parse_direntry(self,inodeoffset):
    
        # print("Reached")
        offset=inodeoffset
        self.ext4_extent_copy['ee_block'] = int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
        self.ext4_extent_copy['ee_len'] = int.from_bytes(self.f[offset+0x04:offset+0x06], byteorder='little')
        self.ext4_extent_copy['ee_start_hi'] = int.from_bytes(self.f[offset+0x06:offset+0x08], byteorder='little')
        self.ext4_extent_copy['ee_start_lo'] = int.from_bytes(self.f[offset+0x08:offset+0x0C], byteorder='little')
        # print(self.ext4_extent_copy['ee_len'])
        offset=self.ext4_extent_copy['ee_start_lo']*4096
        dir_sz = self.ext4_extent_copy['ee_len'] * 4096
        # print("\ndirectory size is",dir_sz,"\n")
        if dir_sz==0: 
            return
        i=0
        while i < dir_sz:
            # print(f"i is {i}")
            dirent_sz=self.ext4_parse_direntry_internal(offset)
            # print(f"Directory Entry Size: {dirent_sz}")
            # print(f"\n{hex(offset)}")
            if int.from_bytes(self.f[offset:offset+0x13], byteorder='little')==0:
                break
            if self.ext4_dir_entry_2['name_len']==2 and self.ext4_dir_entry_2['name']=="..":
                print(f"Inode: {self.ext4_dir_entry_2['inode']}")
                print(f"Record Length: {self.ext4_dir_entry_2['rec_len']}")
                print(f"Name Length: {self.ext4_dir_entry_2['name_len']}")
                print(f"File Type: {self.ext4_dir_entry_2['file_type']}")
                print(f"Name: {self.ext4_dir_entry_2['name']}")
                offset=offset+8
                i=i+8
                continue
            if self.ext4_dir_entry_2['inode'] == 0 and self.ext4_dir_entry_2['rec_len'] > 263 and self.ext4_dir_entry_2['name_len']==0:
                offset=offset+4
                i=i+4
                continue
            # if self.ext4_dir_entry_2['inode'] == 0 and self.ext4_dir_entry_2['rec_len'] ==0 and self.ext4_dir_entry_2['name_len']==0 and self.ext4_dir_entry_2['file_type']==0:
            #     offset=offset+0x04
            #     i=i+0x04
            #     continue
            if self.ext4_dir_entry_2['inode'] > self.maxinode and self.ext4_dir_entry_2['rec_len'] ==0 and self.ext4_dir_entry_2['name_len']==0:
                offset=offset+4
                i=i+4
                continue 
            if self.ext4_dir_entry_2['inode'] == 0 and self.ext4_dir_entry_2['rec_len'] ==12 and self.ext4_dir_entry_2['name_len']==0:
                offset=offset+0x0c
                i=i+0x0c
                continue
            if self.ext4_dir_entry_2['rec_len'] > 263 and self.ext4_dir_entry_2['inode'] < self.ext4_superblock['sb_first_ino'] and self.ext4_dir_entry_2['inode']>0:
                offset=offset+0x08
                i=i+0x08
                continue
            if self.ext4_dir_entry_2['file_type'] == 0:
                offset=offset+8
                i=i+8
                continue
            if self.ext4_dir_entry_2['name_len'] == 0 and self.ext4_dir_entry_2['inode'] != 0:
                offset=offset+0x08
                i=i+0x08
                continue
            if self.ext4_dir_entry_2['rec_len'] > 263 and self.ext4_dir_entry_2['name_len']==0:
                offset=offset+0x08
                i=i+0x08
                continue
            if self.ext4_dir_entry_2['inode'] > self.maxinode:
                offset=offset+4
                i=i+4
                continue
            if dirent_sz==0:
                break                
            if self.ext4_dir_entry_2['rec_len']!=0 and self.ext4_dir_entry_2['name_len']!=0:
               self.ext4_parse_linear_dir_entry_info(offset)
               offset=offset+dirent_sz
            i=i+dirent_sz     
     
    def ext4_parse_linear_dir_entry_info(self,offset):
        self.ext4_dir_entry_2['inode']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
        print(f"Inode: {self.ext4_dir_entry_2['inode']}")
        self.ext4_dir_entry_2['rec_len']=int.from_bytes(self.f[offset+0x04:offset+0x06],byteorder='little')
        print(f"Record Length: {self.ext4_dir_entry_2['rec_len']}")
        self.ext4_dir_entry_2['name_len']=int.from_bytes(self.f[offset+0x06:offset+0x07],byteorder='little')
        print(f"Name Length: {self.ext4_dir_entry_2['name_len']}")
        self.ext4_dir_entry_2['file_type']=int.from_bytes(self.f[offset+0x07:offset+0x08],byteorder='little')
        print(f"File Type: {self.ext4_dir_entry_2['file_type']}")
        try:
            name = self.f[offset+0x08:offset+0x08+self.ext4_dir_entry_2['name_len']].decode('utf-8')
            print(f"Name: {name}")
        except:
            name = self.f[offset+0x08:offset+0x08+self.ext4_dir_entry_2['name_len']].hex()
            print(f"Name: {name}")
        return (offset+self.ext4_dir_entry_2['rec_len'])
        
     
        
    def ext4_parse_direntry_internal(self,offset):
        rec_len=0
        if (self.ext4_inode['i_flags'] & EXT4_INODE_FLAGS['EXT4_INDEX_FL'])&1 == 1: #check for hashed entries
            self.dx_root['dot_inode']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
            # print(f"Inode: {self.dx_root['dot_inode']}")
            self.dx_root['dot_rec_len']=int.from_bytes(self.f[offset+0x04:offset+0x06],byteorder='little')
            # print(f"Record Length: {self.dx_root['dot_rec_len']}")
            rec_len=self.dx_root['dot_rec_len']
            self.dx_root['dot_name_len']=int.from_bytes(self.f[offset+0x06:offset+0x07],byteorder='little')
            # print(f"Name Length: {self.dx_root['dot_name_len']}")
            self.dx_root['dot_file_type']=int.from_bytes(self.f[offset+0x07:offset+0x08],byteorder='little')
            # print(f"File Type: {self.dx_root['dot_file_type']}")
            self.dx_root['dot_name']=self.f[offset+0x08:offset+0x0C].hex()
            # print(f"Name: {self.dx_root['dot_name']}")
            self.dx_root['dot_dot_inode']=int.from_bytes(self.f[offset+0x0C:offset+0x10], byteorder='little')
            # print(f"Inode: {self.dx_root['dot_dot_inode']}")
            self.dx_root['dot_dot_rec_len']=int.from_bytes(self.f[offset+0x10:offset+0x12],byteorder='little')
            # print(f"Record Length: {self.dx_root['dot_dot_rec_len']}")
            rec_len=self.dx_root['dot_dot_rec_len']
            self.dx_root['dot_dot_name_len']=int.from_bytes(self.f[offset+0x12:offset+0x13],byteorder='little')
            # print(f"Name Length: {self.dx_root['dot_dot_name_len']}")
            self.dx_root['dot_dot_file_type']=int.from_bytes(self.f[offset+0x13:offset+0x14],byteorder='little')
            # print(f"File Type: {self.dx_root['dot_dot_file_type']}")
            self.dx_root['dot_dot_name']=self.f[offset+0x14:offset+0x18].hex()
            # print(f"Name: {self.dx_root['dot_dot_name']}")
            self.dx_root['reserved_zero']=int.from_bytes(self.f[offset+0x18:offset+0x1C], byteorder='little')
            # print(f"Reserved Zero: {self.dx_root['reserved_zero']}")
            self.dx_root['hash_version']=int.from_bytes(self.f[offset+0x1C:offset+0x1D], byteorder='little')
            # print(f"Hash Version: {self.dx_root['hash_version']}")
            self.dx_root['info_length']=int.from_bytes(self.f[offset+0x1D:offset+0x1E], byteorder='little')
            # print(f"Info Length: {self.dx_root['info_length']}")  
            self.dx_root['indirect_levels']=int.from_bytes(self.f[offset+0x1E:offset+0x1F], byteorder='little')
            # print(f"Indirect Levels: {self.dx_root['indirect_levels']}")
            self.dx_root['unused_flags']=int.from_bytes(self.f[offset+0x1F:offset+0x20], byteorder='little')
            # print(f"Unused Flags: {self.dx_root['unused_flags']}")
            self.dx_root['limit']=int.from_bytes(self.f[offset+0x20:offset+0x22], byteorder='little')
            # print(f"Limit: {self.dx_root['limit']}")
            self.dx_root['count']=int.from_bytes(self.f[offset+0x22:offset+0x24], byteorder='little')
            # print(f"Count: {self.dx_root['count']}")
            self.dx_root['block']=int.from_bytes(self.f[offset+0x24:offset+0x28], byteorder='little')
            # print(f"Block: {self.dx_root['block']}")
            return self.dx_root['count']
            
        else:
            self.ext4_dir_entry_2['inode']=int.from_bytes(self.f[offset:offset+0x04], byteorder='little')
            # print(f"Inode: {self.ext4_dir_entry_2['inode']}")
            self.ext4_dir_entry_2['rec_len']=int.from_bytes(self.f[offset+0x04:offset+0x06],byteorder='little')
            # print(f"Record Length: {self.ext4_dir_entry_2['rec_len']}")
            rec_len=self.ext4_dir_entry_2['rec_len']
            self.ext4_dir_entry_2['name_len']=int.from_bytes(self.f[offset+0x06:offset+0x07],byteorder='little')    
            # print(f"Name Length: {self.ext4_dir_entry_2['name_len']}")
            self.ext4_dir_entry_2['file_type']=int.from_bytes(self.f[offset+0x07:offset+0x08],byteorder='little')
            # print(f"File Type: {self.ext4_dir_entry_2['file_type']}")
            offset=offset+0x08
            rec_len=self.ext4_dir_entry_2['name_len']+0x08
            for i in range(4, rec_len, 4):
                if i < rec_len and i+4 >= rec_len:
                    rec_len=i+4
                    break
                    # print(f"Name: {self.ext4_dir_entry_2['name']}")
            try:
                self.ext4_dir_entry_2['name'] = self.f[offset:offset+self.ext4_dir_entry_2['name_len']].decode('utf-8')
            except:
                self.ext4_dir_entry_2['name'] = self.f[offset:offset+self.ext4_dir_entry_2['name_len']].hex()
            return rec_len
        
def ext4parser(filepath):
    ext4 = Ext4Parser(filepath)
    ext4.parse_ext4()

console = Console()    
banner()
argparse = ArgumentParser(description=__doc__)
argparse.add_argument("extpart", metavar="EXT4 partition")
args = argparse.parse_args()
filename = args.extpart
filepath = Path.cwd() / filename
if filepath.exists():
    console.print("\n[bold cyan]Start of Parsing...[/bold cyan]\n")
else:
    print(f"\nFile '{filepath}' not found. Please check the file path.\n")
finalstatus = ext4parser(filepath)